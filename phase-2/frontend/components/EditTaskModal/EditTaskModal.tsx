"use client";

import React, { useState, useEffect } from "react";
// import { Task } from "@/lib/types/types";
import { Task } from "../../lib/types/types"; 
import { api } from "../../lib/api/api";
// import { DateTimePicker } from "../DateTimePicker/DateTimePicker";
import { PriorityBadge } from "../PriorityBadge/PriorityBadge";
import { TagChip } from "../TagChip/TagChip";
import { LabelSelector } from "../LabelSelector/LabelSelector";

interface EditTaskModalProps {
  task: Task;
  isOpen: boolean;
  onClose: () => void;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: string) => void;
}

export const EditTaskModal: React.FC<EditTaskModalProps> = ({
  task,
  isOpen,
  onClose,
  onUpdate,
  onDelete,
}) => {
  const [formData, setFormData] = useState<
    Omit<Task, "id" | "user_id" | "created_at" | "updated_at">
  >({
    title: task.title,
    description: task.description || "",
    priority: task.priority,
    tags: [...task.tags],
    label: task.label || null,
    // due_date: task.due_date ? new Date(task.due_date) : null,
    due_date: task.due_date ? new Date(task.due_date) : null,
    is_completed: task.is_completed,
    is_recurring: task.is_recurring,
    recurrence_pattern: task.recurrence_pattern || null,
  });

  const [currentTagInput, setCurrentTagInput] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      // Initialize the due_date properly to preserve the original time
      const initDueDate = task.due_date ? new Date(task.due_date) : null;

      setFormData({
        title: task.title,
        description: task.description || "",
        priority: task.priority,
        tags: [...task.tags],
        label: task.label || null,
        // due_date: initDueDate,
        due_date: initDueDate,
        is_completed: task.is_completed,
        is_recurring: task.is_recurring,
        recurrence_pattern: task.recurrence_pattern || null,
      });
      setErrors({});
    }
  }, [isOpen, task]);

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value, type } = e.target;

    if (type === "checkbox") {
      const checkbox = e.target as HTMLInputElement;
      setFormData((prev) => ({ ...prev, [name]: checkbox.checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }

    // Clear error when user types
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handlePriorityChange = (priority: "high" | "medium" | "low") => {
    setFormData((prev) => ({ ...prev, priority }));
  };

  const handleAddTag = () => {
    if (
      currentTagInput.trim() &&
      formData.tags.length < 10 &&
      !formData.tags.includes(currentTagInput.trim())
    ) {
      setFormData((prev) => ({
        ...prev,
        tags: [...prev.tags, currentTagInput.trim()],
      }));
      setCurrentTagInput("");
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData((prev) => ({
      ...prev,
      tags: prev.tags.filter((tag) => tag !== tagToRemove),
    }));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && currentTagInput.trim()) {
      e.preventDefault();
      handleAddTag();
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = "Title is required";
    } else if (formData.title.length > 255) {
      newErrors.title = "Title must be 255 characters or less";
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = "Description must be 1000 characters or less";
    }

    if (formData.tags.length > 10) {
      newErrors.tags = "Maximum 10 tags allowed";
    }

    if (formData.due_date) {
      const dueDate = new Date(formData.due_date);
      const now = new Date();
      if (dueDate < now) {
        newErrors.due_date = "Due date must be in the future";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Prepare the update data - send all form data since the API expects complete objects for some fields
      // Exclude due_date since date/time editing is disabled
      const updateData: Partial<Task> = {
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        tags: formData.tags,
        label: formData.label,
        is_completed: formData.is_completed,
        is_recurring: formData.is_recurring,
        recurrence_pattern: formData.recurrence_pattern,
      };

      // Log the data being sent for debugging
      console.log("Sending update data:", updateData);

      const updatedTask = await api.updateTask(task.id, updateData);
      console.log("Updated task response:", updatedTask);

      onUpdate(updatedTask);
      onClose();
    } catch (error: any) {
      console.error("Error updating task:", error);

      // Check if it's a network error or a specific API error
      if (error.message && error.message.includes("HTTP error")) {
        setErrors({
          submit: `API Error: ${error.message}. Please check your connection and try again.`,
        });
      } else {
        setErrors({ submit: "Failed to update task. Please try again." });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (
      window.confirm(
        "Are you sure you want to delete this task? This action cannot be undone.",
      )
    ) {
      try {
        await api.deleteTask(task.id);
        onDelete(task.id);
        onClose();
      } catch (error) {
        console.error("Error deleting task:", error);
        setErrors({ submit: "Failed to delete task. Please try again." });
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div
        className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 mx-4 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-xl font-bold text-gray-900 mb-4">Edit Task</h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="title"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                errors.title
                  ? "border-red-500 focus:ring-red-500"
                  : "border-gray-300 focus:ring-indigo-500"
              }`}
              placeholder="Task title"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title}</p>
            )}
          </div>

          <div className="mb-4">
            <label
              htmlFor="description"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Task description"
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600">{errors.description}</p>
            )}
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <div className="flex space-x-2">
              {(["high", "medium", "low"] as const).map((priority) => (
                <button
                  key={priority}
                  type="button"
                  onClick={() => handlePriorityChange(priority)}
                  className={`px-3 py-2 rounded-lg border ${
                    formData.priority === priority
                      ? "bg-indigo-100 border-indigo-500 text-indigo-700"
                      : "border-gray-300 text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <PriorityBadge priority={priority} />
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label
              htmlFor="tags"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Tags
            </label>
            <div className="flex flex-wrap gap-2 mb-2">
              {formData.tags.map((tag, index) => (
                <TagChip
                  key={index}
                  tag={tag}
                  onRemove={() => handleRemoveTag(tag)}
                />
              ))}
            </div>
            <div className="flex">
              <input
                type="text"
                value={currentTagInput}
                onChange={(e) => setCurrentTagInput(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Add a tag..."
              />
              <button
                type="button"
                onClick={handleAddTag}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-r-lg hover:bg-gray-300"
              >
                Add
              </button>
            </div>
            {errors.tags && (
              <p className="mt-1 text-sm text-red-600">{errors.tags}</p>
            )}
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Label
            </label>
            <LabelSelector
              selectedLabel={formData.label || ""}
              onSelect={(label) =>
                setFormData((prev) => ({
                  ...prev,
                  label: label as "work" | "home" | null,
                }))
              }
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Due Date
            </label>
            <p className="text-gray-600 bg-gray-100 rounded p-2">
              {task.due_date
                ? new Date(task.due_date).toLocaleString()
                : "No due date set"}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Date/time editing is disabled
            </p>
          </div>

          <div className="mb-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                name="is_recurring"
                checked={formData.is_recurring}
                onChange={handleInputChange}
                className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span className="ml-2 text-sm text-gray-700">Recurring Task</span>
            </label>

            {formData.is_recurring && (
              <div className="mt-2 ml-6">
                <label
                  htmlFor="recurrence_pattern"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Recurrence Pattern
                </label>
                <select
                  id="recurrence_pattern"
                  name="recurrence_pattern"
                  value={formData.recurrence_pattern || ""}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">Select pattern</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            )}
          </div>

          <div className="flex flex-col sm:flex-row sm:space-x-3 space-y-3 sm:space-y-0 mt-6">
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {isLoading ? "Updating..." : "Update Task"}
            </button>

            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            >
              Cancel
            </button>

            <button
              type="button"
              onClick={handleDelete}
              className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Delete
            </button>
          </div>

          {errors.submit && (
            <p className="mt-3 text-sm text-red-600 text-center">
              {errors.submit}
            </p>
          )}
        </form>
      </div>
    </div>
  );
};
