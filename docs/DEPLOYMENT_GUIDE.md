# Hugging Face Spaces Deployment Guide

## Quick Deployment

### Option 1: Deploy via Hugging Face UI

1. **Create a new Space**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Name: `ai-red-teaming` (or your preferred name)
   - License: MIT
   - SDK: Gradio
   - SDK Version: 4.44.0

2. **Upload files**
   - Upload all files from this directory
   - Ensure `app.py` is in the root
   - Include `requirements.txt`
   - Upload `modules/` folder with all Python modules
   - Upload `taxonomies/` and `datasets/` folders

3. **Configure Space**
   - The Space will auto-build from `app.py`
   - No additional configuration needed

### Option 2: Deploy via Git

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-red-teaming-toolkit
cd ai-red-teaming-toolkit

# Copy toolkit files
cp -r /path/to/11-ai-red-teaming-toolkit/* .

# Add, commit, and push
git add .
git commit -m "Initial deployment of AI Red-Teaming Toolkit"

# For authentication, use your Hugging Face access token:
# Get token from: https://huggingface.co/settings/tokens
# Then push with:
git push -u origin main
# When prompted, use your HF username and token (not password)
```

### Option 3: Use the README_HF.md

Copy the content of `README_HF.md` to create a `README.md` file in your Space. This will be displayed on the Space's landing page.

## File Structure for Deployment

```
your-space/
├── app.py                          # Main Gradio app (REQUIRED)
├── requirements.txt                # Dependencies (REQUIRED)
├── README.md                       # Space description (from README_HF.md)
├── modules/
│   ├── __init__.py                # Make modules importable
│   ├── jailbreak_tester.py
│   ├── prompt_injection.py
│   ├── vulnerability_classifier.py
│   └── report_generator.py
├── taxonomies/
│   ├── owasp_llm_top10.yaml
│   └── mitre_atlas.yaml
└── datasets/
    └── jailbreak_prompts.json
```

## Configuration

### Space Settings

The Space metadata is configured in the README.md frontmatter:

```yaml
---
title: AI Red-Teaming Toolkit
emoji: 🔴
colorFrom: red
colorTo: pink
sdk: gradio
sdk_version: 4.36.1
app_file: app.py
pinned: false
license: mit
---
```

### Hardware Requirements

- **CPU**: Basic (free tier) - Sufficient for this toolkit
- **Memory**: 2GB minimum
- **GPU**: Not required (this toolkit doesn't use ML models)

### Environment Variables

No environment variables required for basic operation.

For API integration (optional):
- `OPENAI_API_KEY` - If testing with OpenAI models
- `ANTHROPIC_API_KEY` - If testing with Claude
- `HF_TOKEN` - For private Spaces

## Testing Your Deployment

1. **Local Testing**
   ```bash
   # Test locally before deploying
   python app.py
   ```
   Access at http://localhost:7860

2. **Space Testing**
   - Wait for Space to build (usually 1-2 minutes)
   - Click "Open Space" button
   - Test each tab to ensure functionality

## Common Issues

### Import Errors

If you see module import errors:

1. Create `modules/__init__.py`:
   ```python
   # modules/__init__.py
   from .jailbreak_tester import JailbreakTester
   from .prompt_injection import PromptInjectionTester
   from .vulnerability_classifier import VulnerabilityClassifier
   from .report_generator import ReportGenerator
   
   __all__ = [
       'JailbreakTester',
       'PromptInjectionTester', 
       'VulnerabilityClassifier',
       'ReportGenerator'
   ]
   ```

2. Update `app.py` imports:
   ```python
   from modules import JailbreakTester, PromptInjectionTester
   from modules import VulnerabilityClassifier, ReportGenerator
   ```

### Build Failures

Check the Space logs for specific errors:
- Verify `requirements.txt` dependencies
- Ensure all files are uploaded
- Check Python syntax errors

**Common Dependency Issues:**

If you encounter `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`:
- This occurs when Gradio 4.36.1+ uses an incompatible version of `huggingface_hub`
- Solution: Pin `huggingface_hub<0.23.0` in `requirements.txt`:
  ```
  gradio==4.36.1
  huggingface_hub<0.23.0
  pyyaml==6.0.1
  ```
- The HfFolder class was removed in `huggingface_hub` 0.23.0+, but Gradio 4.36.1 still requires it

### Performance Issues

If the Space is slow:
- Consider upgrading to a paid tier
- Optimize code for efficiency
- Cache results when possible

## Customization

### Branding

1. Update Space title and emoji in README.md
2. Modify color scheme in `app.py`:
   ```python
   demo = gr.Blocks(theme=gr.themes.Soft())
   ```

3. Add custom CSS:
   ```python
   demo = gr.Blocks(css=".gradio-container {background-color: #f5f5f5}")
   ```

### Features

Enable/disable tabs by commenting out sections in `app.py`:
```python
with gr.Tabs():
    with gr.Tab("🎯 Jailbreak Testing"):
        # ... tab content
    
    # with gr.Tab("💉 Prompt Injection"):  # Disabled
    #     # ... tab content
```

## Security Considerations

### Public Spaces

For public deployment:
- Don't include sensitive API keys
- Add rate limiting if possible
- Include usage disclaimers
- Monitor for abuse

### Private Spaces

For private/team use:
- Set Space to private
- Restrict access to team members
- Enable logging for audit trails

## Monitoring

### Space Analytics

Hugging Face provides:
- View counts
- User engagement metrics
- Error logs in Space settings

### Custom Logging

Add logging to track usage:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_jailbreak_test(...):
    logger.info(f"Jailbreak test initiated: {jailbreak_type}")
    # ... rest of function
```

## Updating Your Space

### Via Git

```bash
cd ai-red-teaming-toolkit
# Make changes
git add .
git commit -m "Update: description of changes"
git push
```

### Via UI

1. Go to Space settings
2. Click "Files" tab
3. Upload updated files
4. Space will auto-rebuild

## Advanced Configuration

### Custom Domain

Link a custom domain:
1. Space Settings → Domains
2. Add your domain
3. Configure DNS records

### Persistent Storage

For saving reports/data:
```python
import os
from pathlib import Path

# Use persistent storage directory
STORAGE_DIR = Path("/data") if os.path.exists("/data") else Path(".")
```

## Integration with Other Tools

### API Access

Gradio spaces can be accessed via API:
```python
from gradio_client import Client

client = Client("YOUR_USERNAME/ai-red-teaming-toolkit")
result = client.predict(
    "gpt-3.5-turbo",  # model_name
    "DAN",            # jailbreak_type
    "test objective", # test_objective
    api_name="/run_jailbreak_test"
)
```

### Embedding

Embed your Space in websites:
```html
<iframe
  src="https://YOUR_USERNAME-ai-red-teaming-toolkit.hf.space"
  frameborder="0"
  width="850"
  height="450"
></iframe>
```

## Support

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Gradio Docs**: https://gradio.app/docs/
- **Community**: https://huggingface.co/spaces

## Example Space

See example deployment at: `https://huggingface.co/spaces/YOUR_USERNAME/ai-red-teaming-toolkit`

---

## Deployment Checklist

- [ ] Create Hugging Face account
- [ ] Create new Space
- [ ] Upload all required files
- [ ] Verify file structure
- [ ] Test locally first
- [ ] Wait for Space to build
- [ ] Test all functionality
- [ ] Add comprehensive README
- [ ] Configure Space settings
- [ ] Share with team/public

**Your Space will be live at:**
`https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

---

*For questions or issues, refer to the main README.md or create an issue on GitHub.*
