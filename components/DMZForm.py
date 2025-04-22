import discord
from discord.ext import commands
from discord.utils import *

dmz_form_channel = 1363551259977584702
rules_channel = 830567020427739166

FORMS_OUTPUT_CHANNEL = 1363554500043870495

# Server Roles
USER_ROLE_ID = 1239939068905914368
MEMBER_ROLE_ID = 852500184662409216

'''
Formulario para desbloquear las opciones de usuario del servidor de discord de Pana Gaming.
'''
class DMZForm(discord.ui.Modal, title="INGRESO A PANA GAMING"):
    quest1 = discord.ui.TextInput(
        label="Pregunta 1",
        required=True,
        max_length=120
    )

    quest2 = discord.ui.TextInput(
        label="Pregunta 2",
        required=True,
        max_length=120
    )

    quest3 = discord.ui.TextInput(
        label="Pregunta 3",
        required=True,
        max_length=230
    )

    async def on_submit(self, interaction: discord.Interaction):
        informes_channel = interaction.guild.get_channel(FORMS_OUTPUT_CHANNEL)
        user_role = interaction.guild.get_role(USER_ROLE_ID)
        member_role = interaction.guild.get_role(MEMBER_ROLE_ID)
        
        user = interaction.user

        if user_role in user.roles or member_role in user.roles:
            await interaction.response.defer()

        else:
            embed = discord.Embed(
                title=f"Nuevo Usuario {user.name}",
                description=f"{user.mention}",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="1. ¿Como has encontrado nuestro servidor de Discord?",
                value=self.quest1.value,
                inline=False
            )
            embed.add_field(
                name="2. ¿Que te ha llamado la atención para unirte a nuestra comunidad Pana Gaming?",
                value=self.quest2.value,
                inline=False
            )
            embed.add_field(
                name="3. ¿Te has leido las normas del servidor de Pana Gaming y la biografía de esta comunidad?,¿Que opinas?",
                value=self.quest3.value,
                inline=False 
            )

            await informes_channel.send(embed=embed)
            await user.add_roles(user_role, reason="Formulario de ingreso a Pana Gaming completado!!!")
        
            confirm_embed = discord.Embed(
                title="BIENVENIDO A LA COMUNIDAD DE PANA GAMING!!!",
                description="Ya eres oficialmente Usuario de la comunidad de Pana Gaming. Ahora puedes disfrutar de nuestro contenido y recuerda que esta comunidad es tu hogar.",
                color=discord.Color.green()
            )
            await user.send(embed=confirm_embed)
            await interaction.response.defer()
