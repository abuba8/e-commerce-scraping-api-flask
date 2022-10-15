import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './index.css'

// assets
import SearchIcon from '../../assets/icons/searchIcon.png'

const Header = () => {

  const [value, setValue] = useState('')

  const onSubmit = async (e) => {
    try {
      e.preventDefault()
      const headers = {
        "Content-Type": "application/json",
      }
      console.log('value', value)
      const result = await  axios.post('http://127.0.0.1:5000/api', {query :value}, {headers} )
      
      console.log('Res', result)
    } catch (e) {
      console.log('Err', e)
    }
  }

  return (
    <>
      <header className='main_header'>
        <div className='header_content_view'>
          <div className='header_content'>
            <h1 style={{ color: '#fff' }}>
              PRICE<span style={{color: '#cccc00'}}>CHECK</span>
            </h1>
            <h2>Home</h2>
            <h2>Stores</h2>
          </div> 
        </div>
      </header>
      <div className='search_bar_view'>
        <div className='search_bar_content'>
          <img className='search_icon' src={SearchIcon} />
          <div type='submit' className='input_view'>
            <form  onSubmit={onSubmit}>
              <input 
                className='input'
                placeholder='search'
                value={value}
                onChange={(e) => setValue(e.target.value)}
              />
            </form>
          </div>
        </div>
      </div>
    </>
  )
}

export default Header