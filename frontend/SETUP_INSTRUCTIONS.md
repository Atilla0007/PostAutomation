# React Component Integration Setup Instructions

## Overview

This project now includes a React frontend with TypeScript, Tailwind CSS, and shadcn/ui components. The `BackgroundPaths` component has been integrated into the codebase.

## Project Structure

The frontend follows the shadcn/ui project structure:

```
PostAutomation/
├── components/
│   ├── ui/              # shadcn/ui components
│   │   ├── background-paths.tsx
│   │   └── button.tsx
│   └── demo.tsx         # Demo component
├── lib/
│   └── utils.ts         # Utility functions (cn helper)
├── app/
│   └── globals.css      # Global styles with Tailwind
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── components.json      # shadcn/ui configuration
```

## Why `/components/ui` is Important

The `/components/ui` directory is the standard location for shadcn/ui components. This structure:

1. **Follows shadcn/ui conventions** - All shadcn components are placed in this directory
2. **Enables easy component management** - Use `npx shadcn-ui@latest add [component]` to add more components
3. **Maintains consistency** - Other developers familiar with shadcn will know where to find components
4. **Supports path aliases** - The `@/components/ui` alias is configured in `tsconfig.json` and `components.json`

## Prerequisites

Before setting up, ensure you have:
- **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
- **npm** or **yarn** package manager

## Setup Steps

### 1. Install Dependencies

Run the following command to install all required npm packages:

```bash
npm install
```

This will install:
- React and Next.js
- TypeScript
- Tailwind CSS and related plugins
- Framer Motion (for animations)
- Radix UI primitives
- Class Variance Authority
- Other required dependencies

### 2. Verify Installation

After installation, verify that all dependencies are installed correctly:

```bash
npm list --depth=0
```

### 3. Configure shadcn/ui (Optional - Already Configured)

The project is already configured with shadcn/ui. The `components.json` file contains the configuration. If you need to reinitialize:

```bash
npx shadcn-ui@latest init
```

**Note:** The current configuration uses:
- Style: `default`
- Base color: `slate`
- CSS variables: `true`
- Component path: `@/components/ui`

### 4. Using the Component

The `BackgroundPaths` component is ready to use. Import it in your React/Next.js pages:

```tsx
import { BackgroundPaths } from "@/components/ui/background-paths"

export default function HomePage() {
  return <BackgroundPaths title="Your Title Here" />
}
```

Or use the demo component:

```tsx
import { DemoBackgroundPaths } from "@/components/demo"

export default function HomePage() {
  return <DemoBackgroundPaths />
}
```

## Component Details

### BackgroundPaths Component

**Location:** `components/ui/background-paths.tsx`

**Props:**
- `title` (optional, string): The title text to display. Default: "Background Paths"

**Features:**
- Animated floating SVG paths
- Letter-by-letter text animation
- Dark mode support
- Fully responsive
- Uses Framer Motion for animations

### Button Component

**Location:** `components/ui/button.tsx`

This is the standard shadcn/ui button component with variants:
- `default`, `destructive`, `outline`, `secondary`, `ghost`, `link`
- Sizes: `default`, `sm`, `lg`, `icon`

## Development

### Running the Development Server

If using Next.js:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
npm start
```

## Dependencies Installed

### Runtime Dependencies
- `react` & `react-dom` - React library
- `next` - Next.js framework (if using Next.js)
- `framer-motion` - Animation library
- `@radix-ui/react-slot` - Radix UI primitives
- `class-variance-authority` - Component variant management
- `clsx` & `tailwind-merge` - Utility functions for className management
- `lucide-react` - Icon library

### Development Dependencies
- `typescript` - TypeScript compiler
- `@types/react`, `@types/react-dom`, `@types/node` - TypeScript type definitions
- `tailwindcss` - Tailwind CSS framework
- `tailwindcss-animate` - Tailwind animation utilities
- `postcss` & `autoprefixer` - CSS processing
- `eslint` & `eslint-config-next` - Code linting

## Troubleshooting

### TypeScript Errors

If you encounter TypeScript errors:
1. Ensure `tsconfig.json` is properly configured
2. Check that path aliases (`@/*`) are working
3. Run `npm install` again to ensure all types are installed

### Tailwind Not Working

If Tailwind styles aren't applying:
1. Verify `tailwind.config.js` includes the correct content paths
2. Ensure `app/globals.css` is imported in your root layout
3. Check that `postcss.config.js` is present

### shadcn/ui Components Not Found

If imports fail:
1. Verify `components.json` has correct aliases
2. Check `tsconfig.json` path mappings
3. Ensure components are in `components/ui/` directory

## Next Steps

1. **Add more shadcn/ui components:**
   ```bash
   npx shadcn-ui@latest add [component-name]
   ```

2. **Customize the theme:**
   - Edit `app/globals.css` for CSS variables
   - Modify `tailwind.config.js` for theme customization

3. **Integrate with Django:**
   - Set up API endpoints in Django
   - Connect React frontend to Django backend
   - Configure CORS if needed

## Additional Resources

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Framer Motion Documentation](https://www.framer.com/motion/)
- [Next.js Documentation](https://nextjs.org/docs)

