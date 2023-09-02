# Cassette.

Utilidad para pasar guiones escritos en [Fountain](https://fountain.io/) a audio.

Ejemplos de uso:

* Cargamos un fichero de guión en formato [Fountain](https://fountain.io/)
  
```bash
cst="corto"
fountain="corto.fountain"
salida="$(pwd)/corto"
cassette run -j load -p "pname=$cst" -p "fountain=$fountain"
```

* Describimos el guión:
  
```bash
cassette run -j describe -p "pname=$cst"
```

* Obtenemos el timeline y lo completamos que las pistas que enlazan escenas
  
```bash
cassette run -j gettimeline -p "pname=$cst.cst"
```

Se puede pasar una plantilla [jinja2](https://jinja.palletsprojects.com/en/3.0.x/templates/) para que se genere el timeline. Por ejemplo una como la siguiente:

> ```bash
> cassette run -j gettimeline -p "pname=$cst.cst" -p "useDefault=path/to/jinjatemplate.yaml"
> ```

```yaml
tags:
  intro: /path/to/intro.wav
  background: /path/to/bg.wav
  end: /path/to/end.wav
  transition: /path/to/transition.wav
characters:

  - id: 1
    voice:
      tts:
        voiceid: 14
      filter:
        - delay:
            delay_seconds: 0.1
        - reverb:
            room_size: 0.5

  - id: 2
    voice:
      tts:
        voiceid: 14
      filter:
        - reverb:
            room_size: 0.1
  - id: 3
    voice:
      tts:
        voiceid: 29
      filter:
        - reverb:
            room_size: 0.1
timeline:
  - type: sound
    track: intro
    duration: 8
    volume: inout
  {%- for scene in scenes %}
  # {{ scene.location }}
  - type: scene
    scene_id: {{ scene.scene_id }}
    background: background
  {%- if not loop.last %}
  # ...
  - type: sound
    track: transition
    duration: 8
    volume: inout
  {%- endif %}
  {% endfor %}
  - type: sound
    track: end
    duration: 8
    volume: inout
```

* Cargamos el timeline al proyecto
  
```bash
cassette run -j loadtimeline -p "pname=$cst" -p "timeline=$cst.cst.yaml"
```

* Renderizamos los dialogos 
  
```bash
cassette run -j renderaudio -p "pname=$cst" -p "storepath=$salida"
```

* Renderizamos las escenas 
  
```bash
cassette run -j renderscene -p "pname=$cst" -p "storepath=$salida"
```

* Renderizamos el guión completo.
  
```bash
cassette run -j renderrecord -p "pname=$cst" -p "storepath=$salida"
```

# Configuración del timeline.

## Voces

A cada caracter identificado por un id se le puede configurar una voz en `voice.tts.voiceid` . Adicionalmete a esta voz se le pueden añadir efectos de audio en la sección `filter`. 

Estos efectos de audio son algunos de los que ofrece la libreria [Spotify Pedalboard](https://spotify.github.io/pedalboard/reference/pedalboard.io.html).

Se tienen disponibles los siguientes:

### Reverb

```yaml
filter:
    ...
    - reverb:
        room_size: 0.5
        damping: 0.5
        wet_level: 0.33
        dry_level: 0.4
        width: 1.0
        freeze_mode: 0.0
```

### Distorsion 

```yaml 
filter:
    ...
    - distortion:
        drive_db: 25
```

### Delay 

```yaml
filter:
    ...
    - delay:
        delay_seconds: 0.5
        feedback: 0.0
        mix: 0.5
```

### Gain 

```yaml
filter:
    ...
    - gain:
        gain_db: 1.0
```

EJEMPLO: 

```yaml
characters:
  # PEDRO
  - id: 1
    voice:
      tts:
        voiceid: 14
      filter:

        - delay:
            delay_seconds: 0.5

        - distortion:
            drive_db: 25
            
        - reverb:
            room_size: 0.1
    
  # MARIA
  - id: 2
    voice:
      tts:
        voiceid: 29
      filter:
        - reverb:
            room_size: 0.1
```

### Voces

> La voz se ha de setear con el id. El id puede variar según sistema operativo.  Para MACOS es el > siguiente:


| Genero | ID | Nombre | Lengua |
|--------|----|--------|--------|
| VoiceGenderFemale |29| Monica |`['es_ES']`| 
| VoiceGenderFemale |31| Paulina |`['es_MX']`| 
| VoiceGenderFemale |37| Tessa |`['en_ZA']`| 
| VoiceGenderMale |14| Jorge |`['es_ES']`| 
| VoiceGenderMale |15| Juan |`['es_MX']`| 
| VoiceGenderMale |8| Diego |`['es_AR']`| 



## Timeline

### Escena

```yaml
  - type: scene
    scene_id: 1
    background: bg
```

### Transición

```yaml 
  - type: sound
    track: sound1
    duration: 8
    volume: inout
```