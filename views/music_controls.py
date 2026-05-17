import discord

class MusicControls(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Pause",
        style=discord.ButtonStyle.gray
    )
    async def pause_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        vc = interaction.guild.voice_client

        if vc and vc.is_playing():

            vc.pause()

            await interaction.response.send_message(
                "⏸️ Music dipause.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Resume",
        style=discord.ButtonStyle.green
    )
    async def resume_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        vc = interaction.guild.voice_client

        if vc and vc.is_paused():

            vc.resume()

            await interaction.response.send_message(
                "▶️ Music dilanjutkan.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Skip",
        style=discord.ButtonStyle.blurple
    )
    async def skip_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        vc = interaction.guild.voice_client

        if vc and vc.is_playing():

            vc.stop()

            await interaction.response.send_message(
                "⏭️ Lagu diskip.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Stop",
        style=discord.ButtonStyle.red
    )
    async def stop_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        vc = interaction.guild.voice_client

        if vc:

            await vc.disconnect()

            await interaction.response.send_message(
                "⏹️ Music dihentikan.",
                ephemeral=True
            )