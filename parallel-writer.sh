#!/bin/bash

# Parallel Law Review Article Writer
# Splits a law review article into independent sections for parallel writing

ARTICLE_TOPIC="$1"
OUTPUT_DIR="./article_sections"

if [ -z "$ARTICLE_TOPIC" ]; then
    echo "Usage: ./parallel-writer.sh \"Article Topic\""
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "🚀 Starting parallel article generation on: $ARTICLE_TOPIC"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Define sections
declare -a SECTIONS=(
    "introduction:Write a comprehensive introduction section for a law review article on '$ARTICLE_TOPIC'. Include background, thesis statement, and roadmap of the article. 2000-2500 words."
    "legal-framework:Write the legal framework section analyzing relevant statutes, regulations, and foundational case law for '$ARTICLE_TOPIC'. 3000-3500 words."
    "historical-analysis:Write a historical development section tracing the evolution of legal doctrine related to '$ARTICLE_TOPIC'. 2500-3000 words."
    "comparative-analysis:Write a comparative analysis section examining how different jurisdictions or courts have approached '$ARTICLE_TOPIC'. 2500-3000 words."
    "policy-implications:Write the policy implications section discussing practical effects and real-world impact of '$ARTICLE_TOPIC'. 2000-2500 words."
    "counterarguments:Write a section addressing counterarguments and responding to critics regarding '$ARTICLE_TOPIC'. 2000-2500 words."
    "conclusion:Write the conclusion section synthesizing findings and proposing solutions or recommendations for '$ARTICLE_TOPIC'. 1500-2000 words."
)

# Launch parallel writing tasks
PIDS=()
for section in "${SECTIONS[@]}"; do
    SECTION_NAME="${section%%:*}"
    SECTION_PROMPT="${section#*:}"
    OUTPUT_FILE="$OUTPUT_DIR/${SECTION_NAME}.md"

    echo "📝 Starting section: $SECTION_NAME"

    # Create a prompt file for Claude
    PROMPT_FILE="$OUTPUT_DIR/.${SECTION_NAME}_prompt.txt"
    echo "$SECTION_PROMPT" > "$PROMPT_FILE"
    echo "" >> "$PROMPT_FILE"
    echo "Format the output as markdown with proper citations and footnotes." >> "$PROMPT_FILE"
    echo "Save the final output to: $OUTPUT_FILE" >> "$PROMPT_FILE"

    # Note: This is a placeholder - in real Conductor usage, you'd launch separate workspaces
    # For now, this creates the structure and prompts

done

echo ""
echo "✅ All section prompts created in $OUTPUT_DIR"
echo ""
echo "📋 Next steps:"
echo "1. Open 7 Conductor workspaces"
echo "2. In each workspace, paste the prompt from the corresponding .txt file"
echo "3. Claude will write each section in parallel"
echo "4. Combine the sections using: ./combine-sections.sh"
echo ""
echo "Section prompts:"
for section in "${SECTIONS[@]}"; do
    SECTION_NAME="${section%%:*}"
    echo "  - $OUTPUT_DIR/.${SECTION_NAME}_prompt.txt"
done
