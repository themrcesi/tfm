import React from 'react'
import "./header.css"

export default function Header() {
    return (
        <div className = "header">
            <img className = "img-centered" src={"https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/Logotipo%20con%20Leyenda/LOGOTIPO%20leyenda%20color%20PNG.png"}></img>
            <h2 className = "center">Uso de Interlinguas para Búsqueda Documental Multilingüe</h2>
        </div>
    )
}
