import { Attributes, Component, ComponentChild, ComponentChildren, FunctionalComponent, h, Ref } from "preact";
import { useEffect, useState } from "preact/hooks";
import style from './style.css';
import { Link } from 'preact-router/match';
import axios from 'axios';
import * as URLCONFIG from "../../../URLCONF.json";

const baseURL = URLCONFIG.endpoint;

interface NFTContract {
    contract_address:string
}

const Collection:FunctionalComponent<NFTContract> = (props: NFTContract) => {
    const {contract_address} = props;
    const [data, setData] = useState({});

    // useEffect(() => {
    //     axios.get(`${baseURL}/contracts/${contract_address}`)
    // }, [])

    return (
        <div class={style.collection}>
            <h1>Collection: {contract_address}</h1>
        </div>
    );
}

export default Collection;
