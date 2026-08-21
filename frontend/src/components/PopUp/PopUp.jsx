import './PopUp.css';

function PopUp({showPopUp, closePopUp, children}){
  if (!showPopUp) {return null}
  return (
    <div className="PopUpOverlay">
      <div className="PopUp" role="dialog" aria-modal="true">
          {children}
          <button onClick={closePopUp}>close</button>
      </div>
    </div>
  );
};

export default PopUp;