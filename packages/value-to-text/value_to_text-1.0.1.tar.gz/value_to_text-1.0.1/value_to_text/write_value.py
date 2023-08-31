
# Escreve por extenso valores monetários até 999 Bilhoes
# Escreve por extenso valores não monetários até 999 Bilhoes
# Escreve por extenso percentual de taxas de juros
# Possui parametros para troca de moeda e ou separadores

# Python Open Source Lib
# By Edenilson Fernandes dos Santos

class Value_to_text:  
            
    def __init__(self):
        self.unidades = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']
        self.especiais = ['dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
        self.dezenas = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
        self.centenas = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
   
    
    def calc_3digitos(self, num: str):
        C = ''   
        num = int(num)             
        num = str(num)
        if int(len(num)) == 3:
            if int(num[-3]) == 1 and int(num[-2:]) == 0: C = 'cem'
            elif int(num[-3]) >= 1 and int(num[-2:]) == 0: C = self.centenas[int(num[-3])] 
            elif int(num[-3]) >= 1 and int(num[-2]) == 0 and int(num[-1]) > 0: C = self.centenas[int(num[-3])] + ' e ' + self.unidades[int(num[-1])]
            elif int(num[-3]) >= 1 and int(num[-2]) == 1 and int(num[-1]) >= 0: C = self.centenas[int(num[-3])] + ' e ' +  self.especiais[int(num[-1])]
            elif int(num[-3]) >= 1 and int(num[-2]) > 0 and int(num[-1]) == 0: C = self.centenas[int(num[-3])] + ' e ' +  self.dezenas[int(num[-2])]
            elif int(num[-3]) >= 1 and int(num[-2]) > 0 and int(num[-1]) > 0: C = self.centenas[int(num[-3])] + ' e ' +  self.dezenas[int(num[-2])] + ' e ' + self.unidades[int(num[-1])]  
        elif int(len(num)) == 2:
            if int(num[-2]) == 1: C = self.especiais[int(num[-1])]
            elif int(num[-2]) > 1 and int(num[-1]) == 0: C = self.dezenas[int(num[-2])]
            elif int(num[-2]) > 1 and int(num[-1]) > 0: C = self.dezenas[int(num[-2])] + ' e ' + self.unidades[int(num[-1])]   
        else:
            C = 'um' if int(num) == 1 else self.unidades[int(num)]
        return C 


    def perc_to_text(self, taxa: float | str, nome_separador: str = 'virgula') -> str:
        '''taxa_texto = perc_to_text(128.09)\n
            cento e vinte e oito virgula zero nove por cento
        ''' 
        
        if isinstance(taxa, float):
            taxa = str(taxa).replace('.', ',')
            if taxa[-2] == ',': taxa = taxa + '0'
        else:
            taxa = str(taxa).replace('.', ',').replace(' ', '')
            if ',' not in taxa: 
                taxa = taxa + ',00'
            elif taxa[-2] == ',': 
                taxa = taxa + '0'
            
        if ',' in taxa:
            valor_aux = taxa.split(',')
            valor_dir = valor_aux[0]
            valor_esq = valor_aux[1]
        else:
            valor_dir = taxa
            valor_esq = '0'   
    
        if int(valor_dir) > 999: return 'erro, valor maximo 999,99 por cento'    
        if int(valor_dir) > 0:
            valor_dir_extenso = ''   
            valor_dir_extenso = self.calc_3digitos(valor_dir)
        else:
            valor_dir_extenso = 'zero'
            
        if int(valor_esq) > 0:
            valor_esq_extenso = ''
            valor_esq_extenso = self.calc_3digitos(valor_esq)
            if valor_esq[-2] == '0': valor_esq_extenso = 'zero ' + valor_esq_extenso
            return valor_dir_extenso + ' ' + nome_separador + ' ' + valor_esq_extenso + ' por cento'
        else:
            return valor_dir_extenso + ' por cento'
            
                    
    def num_to_text(self, numero: float | str, monetario: bool = True, moeda_unit: str ='real', moeda_plural: str ='reais', nome_separador: str = 'virgula') -> str:
        '''valor_texto = num_to_text(100306000000.01)\n
        cem bilhões e trezentos e seis milhões de reais e um centavo
        '''
        C , num , centavos, cents = '0', str(numero), '', '' 
            
        def calc_centavos(cents: str):
            if int(cents[-2]) == 0 and int(cents[-1]) > 0: D = self.unidades[int(cents[-1])]
            elif int(cents[-2]) == 1 and int(cents[-1]) >= 0: D = self.especiais[int(cents[-1])]
            elif int(cents[-2]) > 1 and int(cents[-1]) == 0: D = self.dezenas[int(cents[-2])] 
            else: D = self.dezenas[int(cents[-2])] + ' e ' + self.unidades[int(cents[-1])]    
            return D
        
        num = num.replace('.','').replace(',','.') if '.' in num and ',' in num else num.replace(',', '.')
        if num == '0' or num == '0.0' or num == '0.00': return 'zero'
        num_aux = num.split('.') if '.' in num else ''
        num = str(num_aux[0]) if num_aux != '' else num
        cents = str(num_aux[1]) if num_aux != '' else ''
        cents = cents + '0' if int(len(cents)) < 2 else cents[:2]
                
        if cents != '' and cents != '0' and cents != '00':
            centavos = calc_centavos(cents)
            if monetario:
                centavos = ' e ' + centavos + ' centavo' if cents == '01' else ' e ' + centavos + ' centavos'
            else:
                if cents[-2] == '0':
                    centavos = ' ' + nome_separador + ' zero ' + centavos 
                else:
                    centavos = ' ' + nome_separador + ' ' + centavos 
                
        if not monetario:
            moeda_unit = ''
            moeda_plural = ''

        # Começa a montar as strings de numero para texto  
        if len(num) > 12:
            print('valor numerico muito grande, nao suportado, max 999 bilhoes')
            return 'valor numerico muito grande, nao suportado, max 999 bilhoes'
        elif len(num) > 9:
            C = self.calc_3digitos(num[-3:])
            M = self.calc_3digitos(num[-6:-3])
            ML = self.calc_3digitos(num[-9:-6])  
            BL = self.calc_3digitos(num[:-9])     

            if int(num[-6:-3]) > 0 and int(num[-3:]) == 0: texto_m = ' mil'
            elif int(num[-6:-3]) > 0 and int(num[-3:]) > 0: texto_m = ' mil e '
            else: texto_m = ''
                
            if int(num[-6:-3]) == 0 and int(num[-9:-6]) == 1 and int(num[-3:]) >= 1: texto_ml = ' milhão e '
            elif int(num[-6:-3]) == 0 and int(num[-9:-6]) == 1: texto_ml = ' milhão de'
            elif int(num[-6:-3]) > 0 and int(num[-9:-6]) == 1: texto_ml = ' milhão e '
            elif int(num[-6:-3]) == 0 and int(num[-9:-6]) > 1: texto_ml = ' milhões de'
            elif int(num[-6:-3]) > 0 and int(num[-9:-6]) > 1: texto_ml = ' milhões e '
            else: texto_ml = ''
            
            if int(num) == 1000000000: texto_bl = ' bilhão de'
            elif int(num) > 1000000000 and int(num[-9:]) > 0 and int(num) < 2000000000: texto_bl = ' bilhão e '
            elif int(num) > 1000000000 and int(num[-9:]) == 0: texto_bl = ' bilhões de'
            elif int(num) > 2000000000 and int(num[-9:]) > 0: texto_bl = ' bilhões e '
            else: texto_bl = ''
            
            if not monetario:
                texto_ml = texto_ml.replace(' milhão de', ' milhão')
                texto_ml = texto_ml.replace(' milhões de', ' milhões')
                texto_bl = texto_bl.replace(' bilhão de', ' bilhão')
                texto_bl = texto_bl.replace(' bilhões de', ' bilhões')

            r = BL + texto_bl + ML + texto_ml + M + texto_m + C + ' ' + moeda_plural + centavos if cents != '' else ML + texto_ml + M + texto_m + C + ' ' + moeda_plural
            return r.replace('  ', ' ') 
        elif len(num) > 6:
            C = self.calc_3digitos(num[-3:])
            M = self.calc_3digitos(num[-6:-3])
            ML = self.calc_3digitos(num[:-6])       

            if int(num[-6:-3]) > 0 and int(num[-3:]) == 0: texto_m = ' mil'
            elif int(num[-6:-3]) > 0 and int(num[-3:]) > 0: texto_m = ' mil e '
            else: texto_m = ''
                        
            if int(num) == 1000000: texto_ml = ' milhão de'
            elif int(num) > 1000000 and int(num[-6:]) > 0 and int(num) < 2000000: texto_ml = ' milhão e '
            elif int(num) > 1000000 and int(num[-6:]) == 0: texto_ml = ' milhões de'
            elif int(num) > 2000000 and int(num[-6:]) > 0: texto_ml = ' milhões e '
            else: texto_ml = ''
            
            if not monetario:
                texto_ml = texto_ml.replace(' milhão de', ' milhão')
                texto_ml = texto_ml.replace(' milhões de', ' milhões')
                
            r = ML + texto_ml + M + texto_m + C + ' ' + moeda_plural + centavos if cents != '' else ML + texto_ml + M + texto_m + C + ' ' + moeda_plural
            return r.replace('  ', ' ')  
        elif len(num) > 3:
            C = self.calc_3digitos(num[-3:])
            M = self.calc_3digitos(num[:-3])
            if cents != '': r = M + ' mil ' + moeda_plural if str(num)[-3:] == '000' else M + ' mil e ' + C + ' ' + moeda_plural + centavos
            else: r = M + ' mil ' + moeda_plural if str(num)[-3:] == '000' else M + ' mil e ' + C + ' ' + moeda_plural
            return r.replace('  ', ' ')  
        elif len(num) <= 3:
            C = self.calc_3digitos(num)
            if cents != '' and C == '': r = centavos[2:] 
            elif cents != '': r = C + ' ' + moeda_unit if int(num) == 1 else C + ' ' + moeda_plural + centavos
            else: r = C + ' ' + moeda_unit if int(num) == 1 else C + ' ' + moeda_plural
            return r.replace('  ', ' ') 
        

