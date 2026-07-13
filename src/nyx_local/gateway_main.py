import asyncio
import logging

from nyx_local.core.bootstrap import Bootstrap
from nyx_local.core.settings import Settings
from nyx_local.services.gateway_service import GatewayService


async def _run_gateway(service: GatewayService) -> None:
    try:
        await service.run()
    finally:
        await service.shutdown()


def main() -> None:
    """Run Nyx Local as a resident Nyx OS gateway client."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    bootstrap = Bootstrap()
    try:
        settings = Settings.from_env(require_gateway_token=True)
    except ValueError as error:
        raise SystemExit(str(error)) from None
    bootstrap.initialize(settings)
    if bootstrap.registry is None:
        raise RuntimeError("Bootstrap did not initialize the component registry")
    gateway_service = bootstrap.registry.get("gateway_service")
    if not isinstance(gateway_service, GatewayService):
        raise RuntimeError("Bootstrap did not register GatewayService")

    try:
        asyncio.run(_run_gateway(gateway_service))
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Gateway shutdown requested")
    finally:
        bootstrap.shutdown()


if __name__ == "__main__":
    main()
