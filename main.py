from src.app import App
import uvicorn


# write a main funciton that calls app
def main():
    app = App()
    uvicorn.run(app.api)


if __name__ == "__main__":
    main()
