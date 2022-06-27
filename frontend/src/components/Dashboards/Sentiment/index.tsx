import { FunctionalComponent, h } from "preact";
import style from './style.css';

const Sentiment: FunctionalComponent = () => {
    return (
        <div>
            <h1>
                This is the Sentiment Component.
            </h1>
            <img class={style.logo} src="../../assets/sentiment.png"></img>

        </div>
    );
}

export default Sentiment;
