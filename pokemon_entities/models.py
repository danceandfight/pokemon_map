from django.db import models

class Pokemon(models.Model):
    title = models.CharField(verbose_name="Русское название", 
    							max_length=200)
    image = models.ImageField(verbose_name="Изображение",
    	    					upload_to="pokemon_pics", null=True)
    description = models.TextField(verbose_name="Описание",blank=True)
    title_jp =  models.CharField(verbose_name="Японское название", 
    							max_length=200, blank=True)
    title_en =  models.CharField(verbose_name="Японское название", 
    							max_length=200, blank=True)
    previous_evolution = models.ForeignKey("self",
                                verbose_name="Из кого эволюционирует",
                                blank=True,
                                null=True,
                                related_name="next_evolutions",
                                on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
								verbose_name="Покемон",
                                related_name="pokemon_entities",
    							on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appereared_at = models.DateTimeField(verbose_name="Появляется в",
    							blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name="Исчезает в",
    							blank=True, null=True)
    level = models.IntegerField(verbose_name="Уровень", 
    							blank=True, null=True)
    health = models.IntegerField(verbose_name="Здоровье", 
    							blank=True, null=True)
    strength = models.IntegerField(verbose_name="Атака", 
    							blank=True, null=True)
    defense = models.IntegerField(verbose_name="Защита", 
    							blank=True, null=True)
    stamina = models.IntegerField(verbose_name="Выносливость", 
    							blank=True, null=True)