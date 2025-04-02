import React, { useState } from 'react';
import Alberta from '../assets/Alberta.png';
import BritishColumbia from '../assets/British Columbia.png';
import NewBrunswick from '../assets/New Brunswick.png';
import Newfoundland from '../assets/Newfoundland and Labrador.png';
import NovaScotia from '../assets/Nova Scotia.png';
import Ontario from '../assets/Ontario.png';
import Quebec from '../assets/Quebec.png';
import Saskatchewan from '../assets/Saskatchewan.png';


const provinceImages = {
    Alberta,
    "British Columbia": BritishColumbia,
    "New Brunswick": NewBrunswick,
    "Newfoundland and Labrador": Newfoundland,
    "Nova Scotia": NovaScotia,
    Ontario,
    Quebec,
    Saskatchewan,
  };

function Prediction({ selectedProvince }) {
  const image = provinceImages[selectedProvince];

  return (
    <div className='prediction'>
      <h3>Prediction Temperature for {selectedProvince} 2024–2050</h3>
      {image ? (
        <img src={image}/>
      ) : (
        <p>No image available for {selectedProvince}</p>
      )}
    </div>
  );
}

export default Prediction;