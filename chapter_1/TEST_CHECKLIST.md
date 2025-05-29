# Module 1 Testing Checklist

## Prerequisites
- [ ] Python environment activated: `source ../agent_env/bin/activate`
- [ ] Ollama running: `ollama serve`
- [ ] Qwen2.5 model installed: `ollama pull qwen2.5:7b-instruct-q4_K_M`

## Notebook Tests

### 01_what_is_an_agent.ipynb
- [ ] Opens without errors
- [ ] Visualizations render (radar chart, timeline)
- [ ] Interactive exercises work
- [ ] No code execution (conceptual only)

### 02_react_pattern.ipynb
- [ ] Ollama connection test passes
- [ ] Agent data structures defined
- [ ] LLM integration works
- [ ] Tools execute correctly
- [ ] ReAct agent runs demo tasks

### 03_react_vs_rewoo.ipynb
- [ ] ReWOO implementation loads
- [ ] Token comparison shows 64% reduction
- [ ] Side-by-side execution works

### 04_reflexion_pattern.ipynb
- [ ] Reflexion loop executes
- [ ] Self-improvement demonstrated
- [ ] Memory updates work

### 05_advanced_prompting.ipynb
- [ ] Prompting techniques load
- [ ] Examples execute
- [ ] A/B testing framework works

### 06_reasoning_paradigms.ipynb
- [ ] CoT implementation works
- [ ] ToT visualization renders
- [ ] Comparison metrics show

### 07_evaluation_basics.ipynb
- [ ] Benchmarking code runs
- [ ] Metrics calculate correctly
- [ ] Reality check data displays

## Quick Test Commands

```bash
# Test JSON validity
python -m json.tool 01_what_is_an_agent.ipynb > /dev/null && echo "✅ Valid JSON"

# Run specific notebook
jupyter nbconvert --to notebook --execute 01_what_is_an_agent.ipynb

# Run all tests
python test_notebooks.py
```

## Common Issues & Fixes

1. **Import errors**: 
   - Run: `pip install -r ../requirements.txt`

2. **Ollama not running**:
   - Start: `ollama serve`
   - Check: `curl http://localhost:11434/api/tags`

3. **Model not found**:
   - Install: `ollama pull qwen2.5:7b-instruct-q4_K_M`

4. **Matplotlib issues**:
   - Install: `pip install matplotlib numpy`

## Performance Expectations

- Notebook 1: < 5 seconds (no LLM calls)
- Notebook 2: 30-60 seconds (multiple agent runs)
- Notebooks 3-7: 10-20 seconds each

## Success Criteria

✅ All notebooks open without errors
✅ All code cells execute successfully  
✅ Visualizations render properly
✅ Agent demos complete tasks
✅ No missing dependencies