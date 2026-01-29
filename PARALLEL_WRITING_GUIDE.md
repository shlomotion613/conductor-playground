# Parallel Law Review Article Writing with Conductor

## Quick Start

### Step 1: Generate Section Prompts
```bash
./parallel-writer.sh "Your Article Topic Here"
```

This creates 7 independent section prompts in `./article_sections/`

### Step 2: Open 7 Conductor Workspaces

In Conductor, create 7 workspaces with these names:
1. `article-intro`
2. `article-legal-framework`
3. `article-historical`
4. `article-comparative`
5. `article-policy`
6. `article-counterargs`
7. `article-conclusion`

### Step 3: Paste Prompts

In each workspace, paste the corresponding prompt from:
- `article_sections/.introduction_prompt.txt` → workspace 1
- `article_sections/.legal-framework_prompt.txt` → workspace 2
- `article_sections/.historical-analysis_prompt.txt` → workspace 3
- `article_sections/.comparative-analysis_prompt.txt` → workspace 4
- `article_sections/.policy-implications_prompt.txt` → workspace 5
- `article_sections/.counterarguments_prompt.txt` → workspace 6
- `article_sections/.conclusion_prompt.txt` → workspace 7

### Step 4: Let Claude Work

All 7 Claude agents will work in parallel! Use the monitoring tools:
```bash
# In a separate terminal
python3 claude-thinking-monitor.py
```

### Step 5: Combine Sections

Once all sections are complete:
```bash
./combine-sections.sh
```

This creates `law_review_article.md` with all sections merged in order.

## Benefits of Parallel Writing

- **7x faster**: All sections written simultaneously
- **Better focus**: Each Claude instance focuses on one section
- **Easier review**: Review sections independently
- **Flexibility**: Revise individual sections without affecting others

## Section Breakdown

| Section | Word Count | Focus |
|---------|-----------|-------|
| Introduction | 2000-2500 | Background, thesis, roadmap |
| Legal Framework | 3000-3500 | Statutes, regulations, case law |
| Historical Analysis | 2500-3000 | Evolution of doctrine |
| Comparative Analysis | 2500-3000 | Different jurisdictions |
| Policy Implications | 2000-2500 | Practical effects |
| Counterarguments | 2000-2500 | Addressing critics |
| Conclusion | 1500-2000 | Synthesis, recommendations |

**Total: ~17,000-20,000 words**

## Tips

1. **Be specific in your topic**: The more specific, the better quality output
2. **Provide context**: Add background info to each prompt if needed
3. **Use consistent citation style**: Specify Bluebook, APA, etc. in prompts
4. **Review as you go**: Don't wait for all sections to finish
5. **Edit transitions**: After combining, smooth out section transitions

## Example Usage

```bash
# Generate prompts
./parallel-writer.sh "The Fourth Amendment Implications of AI-Powered Surveillance"

# Monitor progress
python3 claude-thinking-monitor.py

# Get notified when sections complete
python3 conductor-watcher.py

# Combine when done
./combine-sections.sh
```

## Alternative: Manual Workspace Setup

If you prefer manual control, just create 7 workspaces and give each Claude this structure:

```
Write the [SECTION NAME] section for a law review article on [TOPIC].

Requirements:
- [WORD COUNT] words
- [SPECIFIC REQUIREMENTS]
- Proper citations and footnotes
- Save to article_sections/[section-name].md
```

Then combine manually or use the combine script.
