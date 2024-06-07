import { useState } from 'react';
import { Dark, Light } from './components/icons/darklight';

function Header() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  return (
    <>
      <div className="d-flex justify-content-between align-items-center m-2">
        <div >
          <span>Model Used: {}</span><br/>
          <span>Test Error: {}</span>
        </div>
        <div>
          <div onClick={toggleTheme} className="cursor-pointer">
            {isDarkMode ? <Dark /> : <Light />}
          </div>
        </div>
      </div>
    </>
  );
}

export { Header };
