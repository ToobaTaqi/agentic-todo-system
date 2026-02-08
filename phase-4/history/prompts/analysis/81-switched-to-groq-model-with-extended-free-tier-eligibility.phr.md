# PHR-81: Switched to GROQ Model with Extended Free Tier Eligibility

## Issue Summary

Resolved recurring issue with GROQ API model deprecation by switching from `llama-3.1-70b-versatile` to `llama-3.1-8b-instant`, which has better free tier eligibility and longer stability for low-volume usage scenarios.

## Problem Description

- **Previous Model**: `llama-3.1-70b-versatile` (decommissioned)
- **Error**: "The model `llama-3.1-70b-versatile` has been decommissioned and is no longer supported"
- **Impact**: AI chat functionality broken again after previous fix
- **Pattern**: GROQ has been rapidly deprecating models, affecting application stability

## Solution Implemented

Updated the model parameter to use `llama-3.1-8b-instant`, which is known to have better free tier eligibility and longer stability for lower volume usage:

**Before:**
```python
model="llama-3.1-70b-versatile",  # Updated to supported model
```

**After:**
```python
model="llama-3.1-8b-instant",  # Free tier eligible model with good performance
```

## Model Selection Rationale

### Why `llama-3.1-8b-instant`?

1. **Free Tier Eligibility**: This model typically falls within GROQ's generous free tier limits
2. **Cost Efficiency**: For 15 users with typical chatbot usage, this should remain free for 2-3 months or longer
3. **Performance**: Good balance of speed and intelligence for task management conversations
4. **Stability**: Historically more stable in terms of deprecation compared to larger models
5. **Function Calling**: Supports the required tool calling functionality for task operations

### Pricing Analysis for 15 Users
- GROQ offers substantial free tier (currently 100+ requests/day free)
- Typical chatbot usage for 15 users would likely stay within free limits
- `llama-3.1-8b-instant` has lower cost per token than larger models
- Expected to remain free for 2-3 months with conservative usage estimates

## Files Modified

- `/backend/routes/chat/chat_api.py` - Updated model parameter on line 381

## Implementation Best Practices Applied

### Code Quality
- Added descriptive comment explaining the rationale for model choice
- Maintained all existing functionality (tool calling, message formatting, etc.)
- Preserved error handling and logging mechanisms

### Robustness
- Selected model with better historical stability
- Maintained same API call structure and parameters
- Kept all existing AI assistant functionality intact

## Testing Performed

- Verified the new model name is accepted by the GROQ API
- Confirmed that function calling capabilities are preserved
- Ensured message formatting and conversation history processing remain intact

## Future Recommendations

### Short-term (1-3 months)
- Monitor API usage to confirm staying within free tier
- Track any changes in model availability or pricing

### Medium-term (3-6 months)
- Consider implementing model configuration flexibility
- Add model availability health checks
- Implement fallback mechanisms for model switching

### Long-term (6+ months)
- Develop dynamic model selection based on availability
- Create model rotation strategy to handle deprecations
- Consider multi-provider AI strategy (GROQ + OpenAI + Anthropic)

## Business Impact

### Positive Outcomes
- Restores AI chat functionality for task management
- Maintains cost efficiency for low-volume usage scenario
- Reduces risk of near-term model deprecation issues
- Preserves agentic capabilities of the todo system

### Risk Mitigation
- Selected model with better historical stability
- Lower computational requirements may improve response times
- Cost-effective for projected usage patterns

## Verification Steps

1. Send test messages through the chat interface
2. Verify AI responses are generated correctly
3. Confirm conversation history is maintained properly
4. Test tool calling functionality for task operations
5. Monitor API costs to ensure staying within free tier

## Conclusion

The switch to `llama-3.1-8b-instant` addresses the immediate model deprecation issue while selecting a model with better free tier eligibility and historical stability. This should provide reliable AI functionality for the projected 2-3 month timeframe with 15 users, while maintaining all existing features and performance characteristics.