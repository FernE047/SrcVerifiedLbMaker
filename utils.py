def prettifyTime(tempo):
    minutos=int(tempo/60)
    segundos=tempo-60*minutos
    horas=int(minutos/60)
    minutos=minutos-60*horas
    dias=int(horas/24)
    horas=horas-24*dias
    anos=int(dias/365)
    dias=dias-365*anos
    if(dias<365):
        meses=int(dias/31)
        dias=dias-31*meses
    retorno=""
    if(anos>0):
        retorno+=str(anos)+" year"+("s, " if anos>1 else ", ")
    if(meses>0):
        retorno+=str(meses)+" month"+("s, " if meses>1 else ", ")
    if(dias>0):
        retorno+=str(dias)+" day"+("s, " if dias>1 else ", ")
    if(horas>0):
        retorno+=str(horas)+" hour"+("s, " if horas>1 else ", ")
    if(minutos>0):
        retorno+=str(minutos)+" minute"+("s, " if minutos>1 else ", ")
    retorno+=str(segundos)+" seconds"
    return(retorno)
