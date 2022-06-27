import { FunctionalComponent, h } from "preact";

const Sentiment: FunctionalComponent = () => {
    return (
        <header class={style.header}>
        <div>
            <h1>
                This is the Sentiment Component.
            </h1>
            <a href="/">
                <h1>
                    <img class={style.logo} src="../../assets/sentiment.png"></img>
                    DogeTTM<sup>®</sup>
                </h1>
            </a>
        </div>
        </header>
    );
}

export default Sentiment;
