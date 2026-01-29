#!/bin/bash

# Combine Article Sections
# Merges parallel-written sections into a single law review article

OUTPUT_DIR="${1:-./article_sections}"
FINAL_OUTPUT="law_review_article.md"

if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Error: Directory $OUTPUT_DIR not found"
    exit 1
fi

echo "📚 Combining article sections from $OUTPUT_DIR"
echo ""

# Section order
declare -a SECTION_FILES=(
    "introduction.md"
    "legal-framework.md"
    "historical-analysis.md"
    "comparative-analysis.md"
    "policy-implications.md"
    "counterarguments.md"
    "conclusion.md"
)

# Create final article
cat > "$FINAL_OUTPUT" << 'EOF'
# [ARTICLE TITLE]

**Author:** [Your Name]
**Date:** $(date +"%B %Y")

---

EOF

# Combine sections
for section_file in "${SECTION_FILES[@]}"; do
    FULL_PATH="$OUTPUT_DIR/$section_file"

    if [ -f "$FULL_PATH" ]; then
        echo "✅ Adding: $section_file"
        echo "" >> "$FINAL_OUTPUT"
        cat "$FULL_PATH" >> "$FINAL_OUTPUT"
        echo "" >> "$FINAL_OUTPUT"
        echo "---" >> "$FINAL_OUTPUT"
        echo "" >> "$FINAL_OUTPUT"
    else
        echo "⚠️  Missing: $section_file"
    fi
done

# Add bibliography placeholder
cat >> "$FINAL_OUTPUT" << 'EOF'

## Bibliography

[Add compiled citations here]

EOF

echo ""
echo "✅ Article combined successfully!"
echo "📄 Output: $FINAL_OUTPUT"
echo ""
echo "Word count:"
wc -w "$FINAL_OUTPUT"
