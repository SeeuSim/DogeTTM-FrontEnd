import { FunctionalComponent, h } from "preact";
import { useState } from "preact/hooks";
import style from './style.css';

interface RarifyAddress {
    address: string;
}

const Collection:FunctionalComponent<RarifyAddress> = (props: RarifyAddress) => {
    const {address} = props;
    const [data, setData] = useState({});

    return (
        <div class={style.collection}>
            <h1>Collection: {address}</h1>
        </div>
    );
}

export default Collection;
