import logging

from aiohttp import web

logger = logging.getLogger("aioqiwi")


def get_unique(update):
    return (
        f"(bill_id={update.Bill.bill_id})"
        if hasattr(update, "bill_id")  # noqa
        else f"(mid={update.message_id}/hook_id={update.hook_id})"
    )


def not_implemented(*args, **kwargs):
    raise NotImplementedError


class BaseWebHookView(web.View):
    _check_ip = not_implemented
    parse_update = not_implemented

    def validate_ip(self):
        # pulled from aiogram.dispatcher.webhook IP-validator
        if self.request.app.get("_check_ip"):
            ip_address, accept = self.check_ip()
            if not accept:
                logger.warning(f"{ip_address} is not listed as allowed IP")
                raise web.HTTPUnauthorized()

    def check_ip(self):
        forwarded_for = self.request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for, self._check_ip(forwarded_for)

        peer_name = self.request.transport.get_extra_info("peername")

        if peer_name is not None:
            host, _ = peer_name
            return host, self._check_ip(host)

        logger.info("Failed to get IP-address")
        return None, False

    async def post(self):
        """
        Process POST request with validating, further deserialization and resolving BASE
        """
        self.validate_ip()

        update = await self.parse_update()
        await self._resolve_update(update)  # here can be create_task instead of await

        return web.Response(text="ok", status=200)

    async def _resolve_update(self, update):
        unique = get_unique(update)

        logger.info(f"Processing update identified as {unique}")
        for callback, funcs, attr_eq in self.request.app["_dispatcher"].handlers:
            if all(func(update) for func in funcs):
                if attr_eq:
                    if all(
                        getattr(update, key) == attr for key, attr in attr_eq.items()
                    ):
                        self.request.app["_dispatcher"].loop.create_task(
                            callback(update)
                        )

                else:
                    self.request.app["_dispatcher"].loop.create_task(callback(update))
                logger.info(f"Executing {callback.__name__}(:{unique})")
            else:
                logger.info(f"Ignoring {callback.__name__}(:{unique})")
