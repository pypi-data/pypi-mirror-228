# Exemplos de utilizacao da bilioteca value-to-text

```python
# linha1: update pip 
# linha2: install lib value_to_text via pip
python -m pip install --upgrade pip
pip install value-to-text
```

```python
# Escreve por extenso valores monetarios ate 999 Bilhoes
# Escreve por extenso valores nao monetarios ate 999 Bilhoes
# Escreve por extenso percentual de taxas de juros
# Possui parametros para troca de moeda e ou separadores
# Python puro, nao exige demais dependencias de libs externas
```
## import a biblioteca value_to_text
```python
from value_to_text.write_value import Value_to_text
value_to_text = Value_to_text()
```

## metodo num_to_text
# Escreve por extenso valores monetarios ate 999 Bilhoes
```python
text = value_to_text.num_to_text( 100025545465.45 )
print(text)
'''result...
cem bilhoes e vinte e cinco milhoes e quinhentos e quarenta e 
cinco mil e quatrocentos e sessenta e cinco reais e quarenta e cinco centavos
'''

text = value_to_text.num_to_text('9.534,85', moeda_unit='dolar', moeda_plural='dolares')
print(text)
'''result...
nove mil e quinhentos e trinta e quatro dolares e oitenta e cinco centavos
'''

text = value_to_text.num_to_text('9.534,85', monetario=False)
print(text)
'''result...
nove mil e quinhentos e trinta e quatro virgula oitenta e cinco
'''
```

## metodo perc_to_text
# Escreve por extenso percentual de taxas de juros
```python
text = value_to_text.perc_to_text( 0.38 )
print(text)
'''result...
zero virgula trinta e oito por cento
'''

text = value_to_text.perc_to_text( 25.10, nome_separador='ponto')
print(text)
'''result...
vinte e cinco ponto dez por cento
'''
```


