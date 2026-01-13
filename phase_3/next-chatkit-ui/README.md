# OpenAI ChatKit UI

A production-ready chat UI built with Next.js, TypeScript, and the OpenAI API with streaming capabilities.

## Features

- Real-time chat interface with streaming responses
- TypeScript type safety
- Accessibility compliant (ARIA labels, keyboard navigation)
- Responsive design with Tailwind CSS
- Error handling and loading states
- Conversation history management
- MCP-compatible backend integration

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd next-chatkit-ui
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file in the root directory and add your OpenAI API key:
```env
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key_here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Environment Variables

- `NEXT_PUBLIC_OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI integration)
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for your backend API (optional, defaults to '/api')

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Main chat page
├── components/             # React components
│   ├── ChatPage.tsx        # Main chat page component
│   ├── OpenAIChatKitUI.tsx # Main chat interface
│   ├── MessageList.tsx     # Message list display
│   └── MessageInput.tsx    # Message input component
├── services/               # API services
│   └── openai-service.ts   # OpenAI API integration
├── types/                  # TypeScript type definitions
│   └── index.ts            # Type definitions
└── styles/                 # Global styles
    └── globals.css         # Global CSS
```

## API Integration

The application is designed to work with MCP-compatible backend services. By default, it uses the OpenAI API directly, but can be configured to work with your backend API by setting the `NEXT_PUBLIC_API_BASE_URL` environment variable.

## Testing

To run tests:
```bash
npm run test
```

## Building for Production

To build the application for production:
```bash
npm run build
```

Then run the production server:
```bash
npm start
```

## Accessibility Features

This application includes several accessibility features:

- Proper ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Semantic HTML structure
- Focus management
- Color contrast compliance

## License

This project is licensed under the MIT License.