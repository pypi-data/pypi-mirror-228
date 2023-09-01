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

