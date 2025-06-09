// Cloudflare Worker entry point
addEventListener('scheduled', event => {
  event.waitUntil(handleScheduled(event));
});

async function handleScheduled(event) {
  // Initialize the bot
  const bot = new ModernFileDownloaderBot();
  await bot.start();
  
  // Keep the worker alive
  setInterval(() => {
    console.log('Bot is running...');
  }, 60000); // Log every minute
}

// Import the bot class
import { ModernFileDownloaderBot } from './bot.mjs';

export default {
  async fetch(request, env) {
    return new Response('OK', { status: 200 });
  },
};
