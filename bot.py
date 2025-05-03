import discord
from discord.ext import commands
from discord.utils import *

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

dmz_form_channel = 1363551259977584702
rules_channel = 830567020427739166

FORMS_OUTPUT_CHANNEL = 1363554500043870495

# Server Roles
USER_ROLE_ID = 1239939068905914368
MEMBER_ROLE_ID = 852500184662409216
STAFF_ROLE_ID = 856835937816674314
EJECUTIVE_ROLE_ID = 889578160495140898



'''
Formulario para desbloquear las opciones de usuario del servidor de discord de Pana Gaming.
'''
class DMZForm(discord.ui.Modal, title="INGRESO A PANA GAMING"):
    def __init__(self):
        super().__init__(timeout=None)

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
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        ejecutive_role = interaction.guild.get_role(EJECUTIVE_ROLE_ID)
        
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

            await informes_channel.send(
                f"{staff_role.mention} {ejecutive_role.mention}",
                embed=embed
            )
            await user.add_roles(user_role, reason="Formulario de ingreso a Pana Gaming completado!!!")
        
            confirm_embed = discord.Embed(
                title="BIENVENIDO A LA COMUNIDAD DE PANA GAMING!!!",
                description="Ya eres oficialmente Usuario de la comunidad de Pana Gaming. Ahora puedes disfrutar de nuestro contenido y recuerda que esta comunidad es tu hogar.",
                color=discord.Color.green()
            )
            await user.send(embed=confirm_embed)
            await interaction.response.defer()


class DMZFormButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Formulario", style=discord.ButtonStyle.success)
    async def open_form_dmz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DMZForm())


'''
Zona desmilitarizada del servidor de discord.
############################################################################
        ▗▄▄▄  ▗▖  ▗▖▗▄▄▄▄▖    
        ▐▌  █ ▐▛▚▞▜▌   ▗▞▘    
        ▐▌  █ ▐▌  ▐▌ ▗▞▘      
        ▐▙▄▄▀ ▐▌  ▐▌▐▙▄▄▄▖    
############################################################################                   
'''
@bot.event
async def on_ready():
    dmz_form_embed = discord.Embed(
        title="FORMULARIO DE PANA GAMING",
        description="""
            Es importante que respondas a todas las preguntas con toda la sinceridad del mundo ya que Staff tendrá en cuenta todo lo que pongas.
            Abajo tendrás un boton que te habre un formulario y tu tendrás que responder las preguntas.
        """,
        color=discord.Color.green()
    )
    dmz_form_embed.add_field(
        name="1. ¿Como has encontrado nuestro servidor de Discord?",
        value="Pregunta 1",
        inline=False
    )
    dmz_form_embed.add_field(
        name="2. ¿Que te ha llamado la atención para unirte a nuestra comunidad Pana Gaming?",
        value="Pregunta 2",
        inline=False
    )
    dmz_form_embed.add_field(
        name="3. ¿Te has leido las normas del servidor de Pana Gaming?, ¿Que opinas?",
        value="Pregunta 3",
        inline=False 
    )

    dmz_form_channel = bot.get_channel(1363551259977584702)
    await dmz_form_channel.send(
        embed=dmz_form_embed, 
        view=DMZFormButton()
    )
    
@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title="👋 BIENVENIDO A PANA GAMING!",
        description="""
        🎮✨ ¡Hola! Soy tu bot asistente de Pana Gaming. Bienvenido a una comunidad única, en constante evolución y con una visión increíble. Estás a punto de formar parte de algo especial, algo que apenas está comenzando... y tú puedes ayudarnos a construirlo. 💫

        🚧 Actualmente estamos en fase BETA, y tú podrías ser una de las piezas clave para que esta comunidad crezca, mejore y llegue a ser un verdadero hogar para todos los jugadores, soñadores y creadores como tú.

        📝 ¿Quieres desbloquear todas las funciones de la comunidad?
        Solo tienes que rellenar un formulario muy importante que encontrarás en el canal <#1363551259977584702>.
        Tómate tu tiempo, lee cada pregunta con atención y responde con total sinceridad: lo que compartas será tenido muy en cuenta por el Staff de Pana Gaming.

        👀 Pero espera, antes de lanzarte al formulario, te recomendamos que explores los canales que te dejamos justo abajo. Conocerás mejor nuestra visión, nuestras normas y todo lo que hace de Pana Gaming un lugar diferente.
        """,
        color=discord.Color.green()
    )
    embed.add_field(
        name="Biografía de Pana Gaming",
        value="<#1363593707219194167>",
        inline=False
    )
    embed.add_field(
        name="Normas de la Comunidad",
        value="<#830567020427739166>",
        inline=False
    )
    await member.send(embed=embed)

'''
#############################################################################
'''

bot.run("")