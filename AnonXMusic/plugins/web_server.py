from aiohttp import web

# A simple health check route
async def health_check(request):
    return web.Response(text="Bot is running.")

async def index(request):
    return web.Response(text="Welcome to AnonXMusic Bot Web Server.")

# Function to initialize the web server
def start_web_server():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/health", health_check)
    return app

if __name__ == "__main__":
    # Bind the app to an address and port (8080 is commonly used for web apps)
    app = start_web_server()
    web.run_app(app, host="0.0.0.0", port=8080)
