from .play import Play
from .queue import Queue
from .filters import Filters
from .playlists import Playlists
from .nowplaying import NowPlaying

async def setup(bot):

    await bot.add_cog(Play(bot))
    await bot.add_cog(Queue(bot))
    await bot.add_cog(Filters(bot))
    await bot.add_cog(Playlists(bot))
    await bot.add_cog(NowPlaying(bot))