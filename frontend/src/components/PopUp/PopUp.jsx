function PopUp({showPopUp, closePopUp, children}){
  if (!showPopUp) {return null}
  return (
    <div className="PopUp" >
        {children}
        <button onClick={closePopUp}>close</button>
    </div>
  );
};

export default PopUp;