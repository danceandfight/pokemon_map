import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = []

    for pokemon in pokemons:
        url = pokemon.image.url
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': url,
            'title_ru': pokemon.title,
        })
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
        for pokemon_entity in pokemon_entities:
            full_url = request.build_absolute_uri(url)
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title, full_url)

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except HttpResponseNotFound:
        print('<h1>Такой покемон не найден</h1>')

    url = requested_pokemon.image.url

    pokemon_on_page = {
            'pokemon_id': requested_pokemon.id,
            'img_url': url,
            'title_ru': requested_pokemon.title,
            'title_en': requested_pokemon.title_en,
            'title_jp': requested_pokemon.title_jp,
            'description': requested_pokemon.description,
    }

    previous_pokemon = requested_pokemon.previous_evolution
    if previous_pokemon:
        prev_evolution = {
            'title_ru': requested_pokemon.previous_evolution.title,
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': requested_pokemon.previous_evolution.image.url
        }
        pokemon_on_page.update({'previous_evolution': prev_evolution})
    
    next_pokemon = requested_pokemon.next_evolutions.first()
    if next_pokemon:
        next_evolution = {
            'title_ru': next_pokemon.title,
            'pokemon_id': next_pokemon.id,
            'img_url': next_pokemon.image.url
        }
        pokemon_on_page.update({'next_evolution': next_evolution})

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)    

    pokemon_entities = requested_pokemon.pokemon_entities.all()

    for pokemon_entity in pokemon_entities:
        url = pokemon_entity.pokemon.image.url
        full_url = request.build_absolute_uri(url)
        add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                requested_pokemon.title, full_url)

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page,
    })
