import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID
from esphome.components import homeThingApp, image
from esphome.components.homeassistant_media_player import homeassistant_media_player_ns
CONF_MEDIA_PLAYERS = "media_player_group"
CONF_DISPLAY = "display"
CONF_DISPLAY_STATE = "display_state"
CONF_NOW_PLAYING_IMAGE = "now_playing_image"
CONF_NOW_PLAYING_MAX_LINES = "now_playing_max_lines"
CONF_DRAW_NOW_PLAYING_BOTTOM_MENU = "draw_now_playing_bottom_menu"
AUTO_LOAD = ["homeThingApp"]
DEPENDENCIES = ["homeThingApp"]

homething_menu_now_playing_ns = cg.esphome_ns.namespace("homething_menu_now_playing")

HomeThingMenuNowPlayingControl = homething_menu_now_playing_ns.class_("HomeThingMenuNowPlayingControl", cg.Component)

CONF_REMOTE_TRANSMITTER = "remote_transmitter"
CONFIG_SCHEMA = homeThingApp.BASE_SCHEMA.extend(
    {
        cv.GenerateID(CONF_ID): cv.declare_id(HomeThingMenuNowPlayingControl),
        cv.Required(CONF_MEDIA_PLAYERS): cv.use_id(homeassistant_media_player_ns.HomeAssistantMediaPlayerGroup),
        cv.Optional(CONF_NOW_PLAYING_IMAGE): cv.use_id(image.Image_),
        cv.Optional(CONF_NOW_PLAYING_MAX_LINES, default=5): cv.int_,
        cv.Optional(CONF_DRAW_NOW_PLAYING_BOTTOM_MENU, default=False): cv.boolean,
    }
)

async def to_code(config):
    var = await homeThingApp.new_app_base(config)
    cg.add_build_flag("-DUSE_NOW_PLAYING")
    media_players = await cg.get_variable(config[CONF_MEDIA_PLAYERS])
    cg.add(var.set_media_player_group(media_players))

    display_buffer = await cg.get_variable(config[CONF_DISPLAY])
    display_state = await cg.get_variable(config[CONF_DISPLAY_STATE])
    cg.add(var.set_now_playing_display(display_buffer, display_state, media_players))
    cg.add(var.set_now_playing_max_lines(config[CONF_NOW_PLAYING_MAX_LINES]))
    cg.add(var.set_draw_now_playing_bottom_menu(config[CONF_DRAW_NOW_PLAYING_BOTTOM_MENU]))
    
    if CONF_NOW_PLAYING_IMAGE in config:
        cg.add_build_flag("-DUSE_IMAGE")
        now_playing_image = await cg.get_variable(config[CONF_NOW_PLAYING_IMAGE])
        cg.add(var.set_now_playing_image(now_playing_image))

    await cg.register_component(var, config)