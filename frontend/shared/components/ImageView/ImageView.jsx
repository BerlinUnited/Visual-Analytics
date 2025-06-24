import styles from './ImageView.module.css';

const ImageView = ({ imageData }) => {
  if (!imageData) return null;
  
  //console.log("imageData2", imageData)
  return (
    <div className={styles.image_view}>
      <img src={imageData} alt="Fetched content" />
    </div>
  );
};

export default ImageView;