"use client";

import { useState, useEffect, useMemo } from "react";
import { api } from "../../lib/api/api";
import { Task } from "../../lib/types/types";
import ProtectedRoute from "../../components/auth/ProtectedRoute";
import { EditTaskModal } from "../../components/EditTaskModal/EditTaskModal";
import { LabelSelector } from "../../components/LabelSelector/LabelSelector";
import { SearchBar } from "../../components/SearchBar/SearchBar";
import { FilterPanel } from "../../components/FilterPanel/FilterPanel";
import { SortDropdown } from "../../components/SortDropdown/SortDropdown";
import { useNotificationContext } from "../../components/notifications/NotificationProvider";
import { ChatKit } from "../../components/ChatKit/ChatKit";

/* ---------------- TYPES ---------------- */

type SortKey = "due_date" | "priority" | "title" | "created_at";

type NewTaskState = {
  title: string;
  description: string;
  priority: "high" | "medium" | "low";
  tags: string[];
  label: "work" | "home" | null;
  due_date: string;
  is_recurring: boolean;
  recurrence_pattern: "daily" | "weekly" | "monthly" | null;
};

/* ---------------- COMPONENT ---------------- */

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [dateFilter, setDateFilter] = useState("");
  const [labelFilter, setLabelFilter] = useState("");
  const [sortBy, setSortBy] = useState<SortKey>("due_date");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [newTagInput, setNewTagInput] = useState("");

  const [newTask, setNewTask] = useState<NewTaskState>({
    title: "",
    description: "",
    priority: "medium",
    tags: [],
    label: null,
    due_date: "",
    is_recurring: false,
    recurrence_pattern: null,
  });

  const { hasPermission, requestPermission, scheduleNotificationsForTasks } =
    useNotificationContext();

  /* ---------------- DATA ---------------- */

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    if (!tasks.length) return;

    if (!hasPermission) {
      requestPermission();
    } else {
      scheduleNotificationsForTasks(tasks);
    }
  }, [tasks, hasPermission, requestPermission, scheduleNotificationsForTasks]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTasks();
      setTasks(data);
    } catch {
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  /* ---------------- FILTER + SORT ---------------- */

  const filteredTasks = useMemo(() => {
    let result = [...tasks];

    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      result = result.filter(
        (t) =>
          t.title.toLowerCase().includes(q) ||
          t.description?.toLowerCase().includes(q) ||
          t.tags.some((tag) => tag.toLowerCase().includes(q)),
      );
    }

    if (statusFilter) {
      result = result.filter((t) =>
        statusFilter === "completed" ? t.is_completed : !t.is_completed,
      );
    }

    if (priorityFilter) {
      result = result.filter((t) => t.priority === priorityFilter);
    }

    if (labelFilter) {
      result = result.filter((t) => t.label === labelFilter);
    }

    if (dateFilter) {
      const today = new Date();
      const start = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate(),
      );

      result = result.filter((t) => {
        if (!t.due_date) return false;
        const due = new Date(t.due_date);

        if (dateFilter === "overdue") return due < start && !t.is_completed;
        if (dateFilter === "today")
          return due.toDateString() === start.toDateString();

        if (dateFilter === "this-week") {
          const end = new Date(start);
          end.setDate(start.getDate() + 7);
          return due >= start && due <= end;
        }

        if (dateFilter === "this-month") {
          const end = new Date(start);
          end.setMonth(start.getMonth() + 1);
          return due >= start && due <= end;
        }

        return true;
      });
    }

    result.sort((a, b) => {
      let aVal: any;
      let bVal: any;

      if (sortBy === "priority") {
        const order = { high: 3, medium: 2, low: 1 };
        aVal = order[a.priority];
        bVal = order[b.priority];
      } else if (sortBy === "title") {
        aVal = a.title.toLowerCase();
        bVal = b.title.toLowerCase();
      } else if (sortBy === "created_at") {
        aVal = new Date(a.created_at);
        bVal = new Date(b.created_at);
      } else {
        aVal = a.due_date ? new Date(a.due_date) : new Date(8640000000000000);
        bVal = b.due_date ? new Date(b.due_date) : new Date(8640000000000000);
      }

      if (aVal === bVal) return 0;
      return sortOrder === "asc"
        ? aVal > bVal
          ? 1
          : -1
        : aVal < bVal
          ? 1
          : -1;
    });

    return result;
  }, [
    tasks,
    searchQuery,
    statusFilter,
    priorityFilter,
    labelFilter,
    dateFilter,
    sortBy,
    sortOrder,
  ]);

  /* ---------------- ACTIONS ---------------- */

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setError(null);

      const payload = {
        ...newTask,
        is_completed: false,
        due_date: newTask.due_date || undefined,
        recurrence_pattern: newTask.recurrence_pattern || undefined,
      };

      const created = await api.createTask(payload);
      setTasks((prev) => [...prev, created]);

      setNewTask({
        title: "",
        description: "",
        priority: "medium",
        tags: [],
        label: null,
        due_date: "",
        is_recurring: false,
        recurrence_pattern: null,
      });

      setNewTagInput("");
      setShowAddForm(false);
    } catch {
      setError("Failed to create task");
    }
  };

  const toggleCompletion = async (id: string) => {
    try {
      const updated = await api.toggleTaskCompletion(id);
      setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch {
      setError("Failed to update task");
    }
  };

  const deleteTask = async (id: string) => {
    try {
      await api.deleteTask(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch {
      setError("Failed to delete task");
    }
  };

  /* ---------------- RENDER ---------------- */

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-xl text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <button onClick={fetchTasks} className="btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute requireVerified={true}>
      <div className="min-h-screen bg-gray-50 p-4 md:p-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
            <button
              onClick={() => setShowAddForm(!showAddForm)}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              {showAddForm ? "Cancel" : "+ Add Task"}
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Task List Section */}
            <div className="lg:col-span-2">
              {/* Search, Filter and Sort Controls */}
              <div className="mb-6 space-y-4">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div className="w-full md:w-1/3">
                    <SearchBar onSearch={setSearchQuery} />
                  </div>
                  <div>
                    <SortDropdown
                      sortBy={sortBy}
                      sortOrder={sortOrder}
                      onSortChange={(k, o) => {
                        setSortBy(k as SortKey);
                        setSortOrder(o);
                      }}
                    />
                  </div>
                </div>

                <FilterPanel
                  statusFilter={statusFilter}
                  priorityFilter={priorityFilter}
                  dateFilter={dateFilter}
                  labelFilter={labelFilter}
                  onStatusChange={setStatusFilter}
                  onPriorityChange={setPriorityFilter}
                  onDateChange={setDateFilter}
                  onLabelChange={setLabelFilter}
                  onClearFilters={() => {
                    setSearchQuery("");
                    setStatusFilter("");
                    setPriorityFilter("");
                    setDateFilter("");
                    setLabelFilter("");
                  }}
                />
              </div>

              {/* Add Task Form */}
              {showAddForm && (
                <div className="bg-white rounded-xl p-6 mb-8 shadow-lg">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Task</h2>
                  <form onSubmit={handleCreateTask}>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <label htmlFor="title" className="block text-gray-700 mb-1">Title *</label>
                        <input
                          type="text"
                          id="title"
                          value={newTask.title}
                          onChange={(e) => setNewTask(prev => ({...prev, title: e.target.value}))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                          required
                        />
                      </div>
                      <div>
                        <label htmlFor="priority" className="block text-gray-700 mb-1">Priority</label>
                        <select
                          id="priority"
                          value={newTask.priority}
                          onChange={(e) => setNewTask({...newTask, priority: e.target.value as any})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                          <option value="high">High</option>
                          <option value="medium">Medium</option>
                          <option value="low">Low</option>
                        </select>
                      </div>
                    </div>

                    <div className="mb-4">
                      <label htmlFor="description" className="block text-gray-700 mb-1">Description</label>
                      <textarea
                        id="description"
                        value={newTask.description}
                        onChange={(e) => setNewTask(prev => ({...prev, description: e.target.value}))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        rows={3}
                      />
                    </div>

                    <div className="mb-4">
                      <label className="block text-gray-700 mb-1">Tags</label>
                      <div className="flex flex-wrap gap-2 mb-2">
                        {newTask.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="inline-flex items-center bg-indigo-100 text-indigo-800 rounded-full px-3 py-1 text-sm"
                          >
                            {tag}
                            <button
                              type="button"
                              onClick={() => setNewTask(prev => ({
                                ...prev,
                                tags: prev.tags.filter((_, i) => i !== index)
                              }))}
                              className="ml-2 text-indigo-600 hover:text-indigo-800 focus:outline-none"
                            >
                              ×
                            </button>
                          </span>
                        ))}
                      </div>
                      <div className="flex">
                        <input
                          type="text"
                          value={newTagInput}
                          onChange={(e) => setNewTagInput(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' && newTagInput.trim() && newTask.tags.length < 10) {
                              e.preventDefault();
                              if (!newTask.tags.includes(newTagInput.trim())) {
                                setNewTask(prev => ({
                                  ...prev,
                                  tags: [...prev.tags, newTagInput.trim()]
                                }));
                              }
                              setNewTagInput(''); // Clear input
                            }
                          }}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                          placeholder="Press Enter to add tags..."
                        />
                        <button
                          type="button"
                          onClick={() => {
                            if (newTagInput.trim() && newTask.tags.length < 10) {
                              if (!newTask.tags.includes(newTagInput.trim())) {
                                setNewTask(prev => ({
                                  ...prev,
                                  tags: [...prev.tags, newTagInput.trim()]
                                }));
                              }
                              setNewTagInput('');
                            }
                          }}
                          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-r-lg hover:bg-gray-300"
                        >
                          Add
                        </button>
                      </div>
                    </div>

                    <div className="mb-4">
                      <label className="block text-gray-700 mb-1">Label</label>
                      <LabelSelector
                        selectedLabel={newTask.label || ''}
                        onSelect={(label) => setNewTask(prev => ({
                          ...prev,
                          label: label as 'work' | 'home' | null
                        }))}
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <label htmlFor="due_date" className="block text-gray-700 mb-1">Due Date</label>
                        <input
                          type="datetime-local"
                          id="due_date"
                          value={newTask.due_date}
                          onChange={(e) => setNewTask(prev => ({...prev, due_date: e.target.value}))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>

                      <div>
                        <label className="block text-gray-700 mb-1">Recurring</label>
                        <div className="flex items-center space-x-4">
                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={newTask.is_recurring}
                              onChange={(e) => setNewTask(prev => ({...prev, is_recurring: e.target.checked}))}
                              className="mr-2"
                            />
                            <span>Is Recurring?</span>
                          </label>

                          {newTask.is_recurring && (
                            <select
                              value={newTask.recurrence_pattern || ''}
                              onChange={(e) => setNewTask(prev => ({...prev, recurrence_pattern: e.target.value as any || null}))}
                              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            >
                              <option value="">Select pattern</option>
                              <option value="daily">Daily</option>
                              <option value="weekly">Weekly</option>
                              <option value="monthly">Monthly</option>
                            </select>
                          )}
                        </div>
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      Create Task
                    </button>
                  </form>
                </div>
              )}

              {/* Tasks List */}
              {loading ? (
                <div className="flex justify-center items-center h-64">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
                </div>
              ) : filteredTasks.length === 0 ? (
                <div className="bg-white rounded-xl p-12 text-center shadow-lg">
                  <h3 className="text-xl font-medium text-gray-900 mb-2">
                    {tasks.length === 0 ? 'No tasks yet' : 'No tasks match your filters'}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {tasks.length === 0
                      ? 'Get started by creating your first task!'
                      : 'Try changing your search or filter criteria.'}
                  </p>
                  {tasks.length === 0 && (
                    <button
                      onClick={() => setShowAddForm(true)}
                      className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      Create Task
                    </button>
                  )}
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {filteredTasks.map((task) => (
                    <div
                      key={task.id}
                      className={`bg-white rounded-xl p-6 shadow-lg border-l-4 ${
                        task.priority === 'high' ? 'border-red-500' :
                        task.priority === 'medium' ? 'border-yellow-500' : 'border-green-500'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className={`font-semibold ${
                          task.is_completed
                            ? 'text-gray-500 line-through'
                            : 'text-gray-900'
                        }`}>
                          {task.title}
                        </h3>
                        <button
                          onClick={() => toggleCompletion(task.id)}
                          className={`ml-2 px-3 py-1 rounded-full text-xs ${
                            task.is_completed
                              ? 'bg-green-500 text-white'
                              : 'bg-gray-200 text-gray-700'
                          }`}
                        >
                          {task.is_completed ? 'Completed' : 'Mark Done'}
                        </button>
                      </div>

                      {task.description && (
                        <p className="text-gray-600 text-sm mb-3">{task.description}</p>
                      )}

                      <div className="flex flex-wrap gap-2 mb-4">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          task.priority === 'high' ? 'bg-red-100 text-red-800' :
                          task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                        </span>

                        {task.label && (
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            task.label === 'work' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                          }`}>
                            {task.label.charAt(0).toUpperCase() + task.label.slice(1)}
                          </span>
                        )}

                        {task.is_recurring && task.recurrence_pattern && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                            {task.recurrence_pattern}
                          </span>
                        )}

                        {task.tags.map((tag, idx) => (
                          <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                            {tag}
                          </span>
                        ))}
                      </div>

                      {task.due_date && (
                        <div className="text-xs text-gray-600 mb-4">
                          Due: {new Date(task.due_date).toLocaleString()}
                        </div>
                      )}

                      <div className="flex justify-between items-center">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => {
                              setEditingTask(task);
                              setShowEditModal(true);
                            }}
                            className="text-indigo-600 hover:text-indigo-800 text-sm"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => deleteTask(task.id)}
                            className="text-red-500 hover:text-red-700 text-sm"
                          >
                            Delete
                          </button>
                        </div>
                        <div className="text-xs text-gray-500">
                          Created: {new Date(task.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Edit Task Modal */}
              {showEditModal && editingTask && (
                <EditTaskModal
                  task={editingTask}
                  isOpen
                  onClose={() => {
                    setShowEditModal(false);
                    setEditingTask(null);
                  }}
                  onUpdate={(t) =>
                    setTasks((prev) => prev.map((x) => (x.id === t.id ? t : x)))
                  }
                  onDelete={(id) =>
                    setTasks((prev) => prev.filter((t) => t.id !== id))
                  }
                />
              )}
            </div>

            {/* AI Chat Assistant Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-8">
                <ChatKit />
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}