// frontend/config/openaiConfig.js
export const openaiConfig = {
  // OpenAI ChatKit domain key (required for hosted ChatKit)
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || null,

  // OpenAI API key for local development
  apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY || null,

  // Base URL for OpenAI API
  baseUrl: process.env.NEXT_PUBLIC_OPENAI_BASE_URL || 'https://api.openai.com/v1',

  // Model to use for chat completions
  model: process.env.NEXT_PUBLIC_OPENAI_MODEL || 'gpt-3.5-turbo',

  // Configuration for domain allowlist (required for production)
  domainAllowlist: {
    enabled: !!process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
    key: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY
  }
};