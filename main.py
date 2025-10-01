import logging
from contextlib import asynccontextmanager

import htpy as H
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse

from itsdani.logging import ExtraLogger

logging.setLoggerClass(ExtraLogger)
log = logging.getLogger("hcc_server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    log.info("Starting HCC server")

    yield
    # On shutdown
    log.info("Shutting down HCC server")


def exception_qualified_type(exception: Exception) -> str:
    exception_type = type(exception)
    return f"{exception_type.__module__}.{exception_type.__name__}"


async def unknown_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.exception(
        "Internal Server Error",
        extra={
            "exception_type": exception_qualified_type(exc),
            "exception_message": str(exc),
            "exception_status_code": 500,
            "path": request.url.path,
            "query_params": request.query_params,
        },
    )
    return JSONResponse(
        status_code=500,
        content="Unknown error during execution, please contact support.",
    )


app = FastAPI(
    title=__name__,
    exception_handlers={
        Exception: unknown_error_handler,
    },
    lifespan=lifespan,
    
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static", check_dir=False), name="static")


def include_htmx() -> list[H.Element]:
    return [
        H.script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js"),
        H.script(src="https://unpkg.com/htmx.org@1.9.12/dist/ext/json-enc.js"),
    ]


def include_tailwind_css() -> list[H.Element]:
    return [H.script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4")]


def include_franken_ui() -> list[H.VoidElement | H.Element]:
    return [
        H.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/franken-ui@2.1.0-next.16/dist/css/core.min.css",
        ),
        H.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/franken-ui@2.1.0-next.16/dist/css/utilities.min.css",
        ),
        H.script(
            src="https://cdn.jsdelivr.net/npm/franken-ui@2.1.0-next.16/dist/js/core.iife.js",
            type="module",
        ),
        H.script(
            src="https://cdn.jsdelivr.net/npm/franken-ui@2.1.0-next.16/dist/js/icon.iife.js",
            type="module",
        ),
    ]


@app.get("/")
async def root() -> HTMLResponse:
    return HTMLResponse(
        H.html(".text-2xl.lg:text-base")[
            H.head[
                H.title["FastAPI test application"],
                *include_htmx(),
                *include_tailwind_css(),
            ],
            H.body(".bg-background.text-foreground")[
                H.div(".root-layout")[
                    H.p["Hello fastapi"],
                    H.p["hmmm"],
                ],
            ],
        ]
    )
