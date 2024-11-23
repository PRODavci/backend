from utils.unitofwork import IUnitOfWork


class PushTokenService:
    @staticmethod
    async def create(uow: IUnitOfWork, user_id: int, token: str):
        async with uow:
            push_token = await uow.push_token.create({
                'user_id': user_id,
                'token': token,
            })

            await uow.commit()

        return push_token

    @staticmethod
    async def get_list(uow: IUnitOfWork, limit: int = None, offset: int = None, order_by: str = None,
                       reverse: bool = False, **filter_by):
        async with uow:
            push_results = await uow.push_token.get_list(limit, offset, order_by, reverse, **filter_by)

            await uow.commit()

            return push_results
