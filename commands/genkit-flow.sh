#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Create New Genkit Flow${NC}"
echo ""

# Check if we're in a Genkit project
if [ ! -f "package.json" ] || ! grep -q "@genkit-ai/core" package.json; then
    echo -e "${RED}❌ Not in a Genkit project${NC}"
    echo "Run /genkit-init first to create a project"
    exit 1
fi

# Detect language
if [ -f "tsconfig.json" ] || grep -q "typescript" package.json; then
    LANG="typescript"
    EXT="ts"
else
    LANG="javascript"
    EXT="js"
fi

echo -e "${BLUE}Detected $LANG project${NC}"
echo ""

# Get flow details
read -p "Flow name (e.g., chatFlow, summarizeFlow): " FLOW_NAME

if [ -z "$FLOW_NAME" ]; then
    echo -e "${RED}Flow name is required${NC}"
    exit 1
fi

# Convert to camelCase if needed
FLOW_NAME_CAMEL=$(echo "$FLOW_NAME" | sed 's/-\([a-z]\)/\U\1/g' | sed 's/^\([A-Z]\)/\l\1/')

# Determine flow directory
if [ -d "src/flows" ]; then
    FLOW_DIR="src/flows"
elif [ -d "flows" ]; then
    FLOW_DIR="flows"
else
    read -p "Flow directory (default: src/flows): " FLOW_DIR
    FLOW_DIR=${FLOW_DIR:-src/flows}
    mkdir -p "$FLOW_DIR"
fi

FLOW_FILE="$FLOW_DIR/$FLOW_NAME_CAMEL.$EXT"

# Check if flow already exists
if [ -f "$FLOW_FILE" ]; then
    echo -e "${YELLOW}⚠️  Flow file already exists: $FLOW_FILE${NC}"
    read -p "Overwrite? (y/n): " overwrite
    if [[ $overwrite != "y" && $overwrite != "Y" ]]; then
        exit 0
    fi
fi

# Select flow template
echo ""
echo "Select flow template:"
echo ""
echo "  1. Simple Chat - Basic LLM chat flow"
echo "  2. RAG (Retrieval Augmented Generation) - Chat with document context"
echo "  3. Tool Calling - Flow with function/tool calling"
echo "  4. Multi-step - Complex multi-step workflow"
echo "  5. Streaming - Streaming response flow"
echo "  6. Empty - Blank flow template"
echo ""
read -p "Choose (1-6): " TEMPLATE_CHOICE

case $TEMPLATE_CHOICE in
    1)
        # Simple Chat Flow
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({
      message: z.string().describe('User message'),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    const result = await claude35Sonnet.generate({
      prompt: input.message,
    });

    return result.text;
  }
);
EOF
        echo -e "${GREEN}✅ Created simple chat flow${NC}"
        ;;

    2)
        # RAG Flow
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({
      question: z.string().describe('User question'),
      documents: z.array(z.string()).describe('Context documents'),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    // Combine documents into context
    const context = input.documents.join('\\n\\n');

    const prompt = \`Context:\\n\${context}\\n\\nQuestion: \${input.question}\\n\\nAnswer based on the context above:\`;

    const result = await claude35Sonnet.generate({
      prompt: prompt,
    });

    return result.text;
  }
);
EOF
        echo -e "${GREEN}✅ Created RAG flow${NC}"
        ;;

    3)
        # Tool Calling Flow
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { defineTool } from '@genkit-ai/ai';
import { z } from 'zod';

// Define a tool
const weatherTool = defineTool(
  {
    name: 'getWeather',
    description: 'Get weather information for a location',
    inputSchema: z.object({
      location: z.string(),
    }),
    outputSchema: z.object({
      temperature: z.number(),
      conditions: z.string(),
    }),
  },
  async (input) => {
    // TODO: Implement actual weather API call
    return {
      temperature: 72,
      conditions: 'sunny',
    };
  }
);

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({
      message: z.string(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    const result = await claude35Sonnet.generate({
      prompt: input.message,
      tools: [weatherTool],
    });

    return result.text;
  }
);
EOF
        echo -e "${GREEN}✅ Created tool calling flow${NC}"
        ;;

    4)
        # Multi-step Flow
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({
      topic: z.string(),
    }),
    outputSchema: z.object({
      outline: z.string(),
      content: z.string(),
      summary: z.string(),
    }),
  },
  async (input) => {
    // Step 1: Generate outline
    const outlineResult = await claude35Sonnet.generate({
      prompt: \`Create a brief outline for an article about: \${input.topic}\`,
    });

    // Step 2: Generate full content
    const contentResult = await claude35Sonnet.generate({
      prompt: \`Write a detailed article based on this outline:\\n\${outlineResult.text}\`,
    });

    // Step 3: Generate summary
    const summaryResult = await claude35Sonnet.generate({
      prompt: \`Summarize this article in 2-3 sentences:\\n\${contentResult.text}\`,
    });

    return {
      outline: outlineResult.text,
      content: contentResult.text,
      summary: summaryResult.text,
    };
  }
);
EOF
        echo -e "${GREEN}✅ Created multi-step flow${NC}"
        ;;

    5)
        # Streaming Flow
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({
      message: z.string(),
    }),
    outputSchema: z.string(),
    streamSchema: z.string(),
  },
  async (input, streamingCallback) => {
    let fullResponse = '';

    const { response, stream } = await claude35Sonnet.generateStream({
      prompt: input.message,
    });

    for await (const chunk of stream) {
      fullResponse += chunk.text;
      if (streamingCallback) {
        streamingCallback(chunk.text);
      }
    }

    return fullResponse;
  }
);
EOF
        echo -e "${GREEN}✅ Created streaming flow${NC}"
        ;;

    6)
        # Empty template
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({
      // Define your input schema here
    }),
    outputSchema: z.object({
      // Define your output schema here
    }),
  },
  async (input) => {
    // TODO: Implement your flow logic

    return {};
  }
);
EOF
        echo -e "${GREEN}✅ Created empty flow template${NC}"
        ;;

    *)
        echo -e "${RED}Invalid choice, creating empty template${NC}"
        cat > "$FLOW_FILE" << EOF
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${FLOW_NAME_CAMEL} = defineFlow(
  {
    name: '${FLOW_NAME_CAMEL}',
    inputSchema: z.object({}),
    outputSchema: z.object({}),
  },
  async (input) => {
    return {};
  }
);
EOF
        ;;
esac

echo ""
echo -e "${BLUE}Flow created: $FLOW_FILE${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Edit $FLOW_FILE to customize your flow"
echo "  2. Import and export the flow in your main index file:"
echo ""
if [ -f "src/index.$EXT" ]; then
    echo "     // In src/index.$EXT"
else
    echo "     // In your main index file"
fi
echo "     import { ${FLOW_NAME_CAMEL} } from './$FLOW_DIR/${FLOW_NAME_CAMEL}';"
echo "     export { ${FLOW_NAME_CAMEL} };"
echo ""
echo "  3. Run /genkit-run to test your flow in the developer UI"

# Offer to add import to index file
if [ -f "src/index.$EXT" ]; then
    echo ""
    read -p "Add import to src/index.$EXT automatically? (y/n): " add_import
    if [[ $add_import == "y" || $add_import == "Y" ]]; then
        # Calculate relative path
        REL_PATH="./flows/${FLOW_NAME_CAMEL}"

        # Add import and export
        echo "" >> "src/index.$EXT"
        echo "import { ${FLOW_NAME_CAMEL} } from '$REL_PATH';" >> "src/index.$EXT"
        echo "export { ${FLOW_NAME_CAMEL} };" >> "src/index.$EXT"

        echo -e "${GREEN}✅ Added to src/index.$EXT${NC}"
    fi
fi
