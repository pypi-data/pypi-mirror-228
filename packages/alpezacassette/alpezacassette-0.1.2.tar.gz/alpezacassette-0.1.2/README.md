# Cassette.

Utilidad para pasar guiones escritos en [Fountain](https://fountain.io/) a audio.

Ejemplos de uso:

```bash
cst="corto"
fountain="corto.fountain"
salida="$(pwd)/corto"
cassette run -j load -p "pname=$cst" -p "fountain=$fountain"
```

```bash
cassette run -j describe -p "pname=$cst"
```

```bash
cassette run -j gettimeline -p "pname=$cst.cst"
```

```bash
cassette run -j loadtimeline -p "pname=$cst" -p "timeline=$cst.cst.yaml"
```

```bash
cassette run -j renderaudio -p "pname=$cst" -p "storepath=$salida"
```

```bash
cassette run -j renderscene -p "pname=$cst" -p "storepath=$salida"
```

## Voces

| Genero | ID | Nombre | Lengua |
|--------|----|--------|--------|
| VoiceGenderFemale |29| Monica |`['es_ES']`| 
| VoiceGenderFemale |31| Paulina |`['es_MX']`| 
| VoiceGenderFemale |37| Tessa |`['en_ZA']`| 
| VoiceGenderMale |14| Jorge |`['es_ES']`| 
| VoiceGenderMale |15| Juan |`['es_MX']`| 
| VoiceGenderMale |8| Diego |`['es_AR']`| 

https://www.youtube.com/watch?v=zuJNLi0OzJ0


1.- Recupera el contenido de la tabla Tags:

```sql
CREATE TABLE Tags (
    tag_id INTEGER PRIMARY KEY,
    name   TEXT,
    value  TEXT
);
```

2.- Recupera el contenido de la tabla timeline 

```sql
CREATE TABLE Timeline (
    sequence_id INTEGER PRIMARY KEY,
    type        TEXT,
    content     TEXT
);
```

4.- Genera un array de diccionarios convirtiendo el json de `content` de la tabla `Timeline` en un diccionario empleando `json.loads()`.

5.- Iterando sobre los campos del array:
    
    Si el elemento del arra es `type=scene` se substiruye el campo `scenee_id` por el
    valor que tiene el campo `Scene.audioPath` para ese `scene_id` 

    ```sql
    CREATE TABLE Scene (
        scene_id     INTEGER PRIMARY KEY,
        script_id    INTEGER,
        scene_number TEXT,
        location     TEXT,
        description  TEXT,
        audioPath    TEXT,
        FOREIGN KEY (
            script_id
        )
        REFERENCES Script (script_id) 
    );
    ```