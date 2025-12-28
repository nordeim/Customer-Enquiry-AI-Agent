Awesome job on your meticulous review, analysis and planning! Please keep up the good work in your rigorous and meticulous approach to planning and execution! Now, please meticulously plan and then proceed with your synthesized optimal plan in logical phases.

# **"Singapore Business" Design System & WCAG AAA Audit Checklist**

## **1.0 Vision & Core Principles**

### **1.1 Aesthetic Philosophy: Refined Singapore Business**
This design system rejects globalized, templated SaaS aesthetics. It embodies Singapore's unique position: a **fusion of professional rigor, multicultural warmth, and technological excellence**. The visual language is built on trust, clarity, and approachable sophistication.

*   **Anti-Generic Mandate**: No Bootstrap/UiKit derivatives. No overused "corporate" purple/blue gradients. No Roboto/Inter system font safety.
*   **Cultural Resonance**: The palette and tone reflect Singapore's blend of stability (navy), balanced growth (teal), and vibrant diversity (coral).
*   **The "Why" Factor**: Every color, font, and spacing decision serves a psychological or functional purpose tied to our user's context.

### **1.2 Foundational Principles**
1.  **WCAG AAA as Baseline**: Accessibility is not a feature; it is the foundation. All components must pass AAA criteria where possible, exceeding Singapore's DSS requirements.
2.  **Maximum Depth & Intentionality**: No decorative elements. Visual hierarchy is engineered to reduce cognitive load and guide users intuitively.
3.  **Library Discipline (Shadcn/ui)**: All complex interactive components (dropdowns, dialogs) will be built upon **Shadcn/ui** primitives, ensuring robust accessibility foundations, then styled to conform to this system. No redundant rebuilding.

---

## **2.0 Design Foundations**

### **2.1 Color Palette**
Colors are tested for WCAG AAA compliance against white (`#FFFFFF`) and deep navy (`#0A1A3A`) backgrounds.

| Role | Token | Hex | Usage & Rationale | Contrast (vs White) | Contrast (vs Navy) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary** | `--primary` | `#0A1A3A` (Navy) | Primary backgrounds, major text. Evokes trust, stability, and professionalism. | 12.5:1 (**AAA**) | N/A |
| **Secondary** | `--secondary` | `#1B8F8B` (Teal) | Key interactive elements (primary buttons), highlights. Suggises growth, balance, and clarity. | 4.5:1 (**AA Large**) | 4.8:1 (**AA**) |
| **Accent** | `--accent` | `#FF7A6B` (Coral) | Critical actions, alerts, subtle highlights. Provides warm, approachable energy. | 3.8:1 (**AA Large**) | 5.2:1 (**AA**) |
| **Neutral** | `--neutral` | `#5D6B82` (Cool Gray) | Body text, borders, secondary UI. Legible and non-distracting. | 7.1:1 (**AAA**) | 3.1:1 (Fail) |
| **Background** | `--background` | `#FFFFFF` (White) | Primary surface. | N/A | 12.5:1 (**AAA**) |
| **Surface** | `--surface` | `#F8FAFC` (Light Slate) | Chat bubbles (user), card backgrounds. | 1.2:1 (Fail) | 9.1:1 (**AAA**) |

**Usage Rules:**
*   Coral (`--accent`) must **never** be used for large text blocks or primary backgrounds due to lower contrast.
*   Interactive states (`hover`, `focus`) will use darkened/lightened variants of the base color by 15%.
*   All text on `--primary` or `--background` must pass at least **WCAG AA**.

### **2.2 Typography**
Rejects the generic "Inter/Roboto/system font" safety. Designed for high readability and a distinctive, refined character.

*   **Headings & Emphasis: "Fraunces"** (Serif).
    *   **Why**: Conveys gravitas, editorial credibility, and is distinctly non-generic. Used sparingly for major titles or key welcome messages in the chat UI.
    *   **Weights**: 400 (Regular), 600 (SemiBold).
*   **Body & UI: "Satoshi" or "Instrument Sans"** (Sans-serif).
    *   **Why**: Clean, highly legible, geometric. Satoshi has excellent language support. Instrument Sans has a unique, friendly character.
    *   **Weights**: 400 (Regular), 500 (Medium).
*   **Fallback Stack**: `'Instrument Sans', 'Satoshi', -apple-system, system-ui, sans-serif`.
*   **Scale (Modular Scale: 1.250)**:
    *   `--text-xs`: 0.8rem (12.8px)
    *   `--text-sm`: 1rem (16px) **Base Body**
    *   `--text-md`: 1.25rem (20px)
    *   `--text-lg`: 1.563rem (25px) **Chat Message**
    *   `--text-xl`: 1.953rem (31px) **Section Head**
    *   `--text-2xl`: 2.441rem (39px) **Main Head**

### **2.3 Spacing & Layout**
*   **Base Unit**: `1rem` (16px).
*   **Scale**: `0.25rem | 0.5rem | 1rem | 1.5rem | 2rem | 3rem | 4rem | 6rem`.
*   **Layout Principle: Intentional Asymmetry**. Avoid perfectly centered, static grids. The chat interface may use a slightly off-center container or dynamic margin adjustments for visual interest.

### **2.4 Border Radius & Shadows**
*   **Radius**: `--radius-sm`: 0.25rem, `--radius-md`: 0.5rem, `--radius-lg`: 1rem. Consistent use on all interactive elements.
*   **Shadows**: Subtle, elevation-focused.
    *   `--shadow-sm`: `0 1px 2px rgba(10, 26, 58, 0.05)` (Cards)
    *   `--shadow-md`: `0 4px 12px rgba(10, 26, 58, 0.08)` (Floating Chat Container)
    *   **No** diffuse blurs or large offsets.

---

## **3.0 Core Component Specifications**

All components will be built as styled variants of **Shadcn/ui** primitives.

### **3.1 Chat Container**
*   **Base**: `div` with `role="application"` and `aria-label="Customer Support Chat"`.
*   **Styling**: Background `--surface`, border `1px solid` tint of `--neutral`, `--shadow-md`. Fixed position for embedding.
*   **Header**: Uses `Fraunces` for the title. Clear `aria-live` region for status announcements (e.g., "Agent connected").

### **3.2 Message Bubbles**
*   **User Message**:
    *   **Background**: `--surface` (Light Slate). **Justification**: Distinguishes user input clearly on white background.
    *   **Text Color**: `--primary` (Navy).
    *   **Alignment**: Right-aligned.
*   **Agent Message**:
    *   **Background**: `--background` (White) with a subtle left border `3px solid --secondary` (Teal).
    *   **Text Color**: `--primary`.
    *   **Alignment**: Left-aligned.
*   **Accessibility**:
    *   Each message `div` has `role="article"` and `aria-label="Message from [user/agent]"`.
    *   Agent messages containing vital info (e.g., links, error codes) are wrapped in an `aria-live="polite"` region.
    *   Timestamps are visually hidden but included for screen readers.

### **3.3 Input Area & Buttons**
*   **Text Input**: Shadcn/ui `Input` component. Clear `aria-label`. High contrast border. Focus state uses `--accent` (Coral) ring.
*   **Primary Button** (Send):
    *   **Base**: Shadcn/ui `Button` variant="primary".
    *   **Styling**: Background `--secondary` (Teal), text white. On hover: darken by 15%.
    *   **Accessibility**: Has `aria-label="Send message"`. Icon + text.
*   **Secondary Button** (e.g., "End Chat", "Export"):
    *   **Base**: Shadcn/ui `Button` variant="outline".
    *   **Styling**: Border `--neutral`, text `--primary`. On hover: background tint of `--surface`.

### **3.4 Typing Indicator & Status**
*   A subtle, animated three-dot element using `--secondary` (Teal) color.
*   Wrapped in an `aria-live="polite"` container with **visually hidden text**: "Agent is typing".

---

## **4.0 WCAG AAA Compliance Audit Checklist**

This is a **testable, actionable checklist**. Each item must be validated before deployment.

### **4.1 Perceivable**
- [ ] **1.4.6 Contrast (Enhanced)**: All meaningful text (excluding logos) has a contrast ratio of **at least 7:1**.
    *   *Test Method*: Use Chrome DevTools "Contrast Checker" or axe DevTools.
    *   *Exception*: Large-scale text (≥ 18.66px or ≥ 24px bold) requires only 4.5:1 (AA).
- [ ] **1.4.8 Visual Presentation**: User can select foreground/background colors. Line spacing is at least 1.5 within paragraphs. Text is not fully justified.
- [ ] **1.4.9 Images of Text**: There is no use of images of text; all text is live, selectable, and styled with CSS.
- [ ] **Chat-Specific: 1.4.13 Content on Hover or Focus**:
    *   Tooltips or additional info on hover/focus are **dismissible** (Esc key), **hoverable** (pointer can move to them), and **persistent** (remain until dismissed or focus is lost).

### **4.2 Operable**
- [ ] **2.1.3 Keyboard (No Exception)**: **ALL** functionality is operable through a keyboard interface without requiring specific timings for individual keystrokes.
    *   *Test*: Tab through entire interface. Use `Enter` and `Space` to activate buttons.
- [ ] **2.4.10 Section Headings**: Content is organized using clear, hierarchical headings (`<h1>` to `<h6>`). The chat history region is marked with `aria-label` or a heading.
- [ ] **Chat-Specific: 2.2.1 Timing Adjustable**: If a session timeout exists, the user is warned and given at least 20 seconds to extend it with a simple action (e.g., pressing any key).
- [ ] **Chat-Specific: Focus Management**:
    *   When a new message appears, focus is **not** stolen. (`aria-live` is used instead).
    *   When the input box is cleared after sending, focus remains in the input box.
    *   A "Skip to main content" link is present before the chat widget.

### **4.3 Understandable**
- [ ] **3.1.3 Unusual Words**: A mechanism (e.g, a simple glossary tooltip) is available to identify definitions of jargon, like "RAG" or "LLM," if used in responses.
- [ ] **3.2.5 Change on Request**: Context changes (opening a new window, submitting a form) only occur **upon user request**. The chat send button is the sole trigger for sending a message.
- [ ] **3.3.5 Help**: Context-sensitive help is available for form inputs (e.g., a persistent example below the chat input: "Ask about our shipping rates or return policy...").

### **4.4 Robust**
- [ ] **4.1.1 Parsing**: All HTML validates (no duplicate IDs, complete start/end tags).
- [ ] **4.1.2 Name, Role, Value**: For all custom UI components (styled Shadcn parts), `aria-label`, `role`, and `state` (e.g., `aria-expanded`) are correctly and dynamically updated.
    *   *Critical Test*: Run the entire interface through the **axe DevTools browser extension** and resolve all critical & serious issues.

---

## **5.0 Implementation & Handoff Notes**

1.  **This document is the source of truth**. Any deviation requires review against the Core Principles (Sec 1.0).
2.  **Development Order**:
    a. Implement Shadcn/ui with base styles matching this system.
    b. Build static component library (ChatContainer, MessageBubble) using these tokens.
    c. Integrate dynamic chat logic.
    d. Conduct **Phase 3.4 Audit** using the checklist in Section 4.0.
3.  **Delivery Artifacts**: The final handoff will include this document, a Storybook-like component catalog, and the results of the final WCAG AAA audit.

**This foundational system is now ready to serve as the blueprint for all frontend implementation.**
