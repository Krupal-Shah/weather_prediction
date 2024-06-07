function Body() {
  return (
    <>
      <div className="">
        <div className='container border border-dark rounded-4 w-75'>
          <div className='row'>
            <div className='col'>
              <h1 className="text-center">Weather Prediction</h1>
            </div>
          </div>
          <div className='container text-center mt-4'>
            <div className='row'>
              <div className='col'>
                <h3>Today's Weather</h3>
              </div>
            </div>
            <div className='row'>
              <div className='col'>
                {/* <WeatherIcon /> */}
              </div>
              <div className='col'>
                <h2>Sunny</h2>
                <h3>Temperature: 25&deg;C</h3>
                <h5>Location: Edmonton, AB</h5>
              </div>
            </div>
          </div>
          <div className='container text-center mt-4'>
            <div className='row'>
              <div className='col'>
                <h3>Predicted Forecast for Tomorrow</h3>
              </div>
            </div>
            <div className='row'>
              <div className='col'>
                {/* <WeatherIcon /> */}
              </div>
              <div className='col'>
                <h2>Rainy</h2>
                <h3>Temperature: 12&deg;C</h3>
                <h5>Location: Edmonton, AB</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export { Body }