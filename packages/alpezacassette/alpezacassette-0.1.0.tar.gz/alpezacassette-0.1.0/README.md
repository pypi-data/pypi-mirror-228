python setup.py sdist


```
python3.9 setup.py sdist
pip3.9 install ./dist/cassette-1.0.0.tar.gz
```

```bash
export template="/Users/alvaroperis/Dropbox/cinemawritter/out/template.yaml"
export fount="/Users/alvaroperis/Dropbox/cinemawritter/out/guion.fountain"
export out="/Users/alvaroperis/Dropbox/cinemawritter/out"
cassette rscenes --config "$template" --fountain "$fount" --outdir "$out"
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


