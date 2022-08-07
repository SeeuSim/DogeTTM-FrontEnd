import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import * as URLCONFIG from "../../../URLCONF.json";
import PriceGraph from '../../components/Graphs/Price';
import style from './style.css';

const baseURL = URLCONFIG.endpoint;

interface NFTContract {
    contract_address:string
}

interface RarityContract {
    "address":string,
    "name":string,
    "unique_owners":string,
    "tokens":string,
    "description":string,
    "id":string
}

const Collection:FunctionalComponent<NFTContract> = (props: NFTContract) => {
    const {contract_address} = props;
    const [data, setData] = useState<RarityContract>();
    const [loaded, setLoaded] = useState<Boolean>(false);
    const [time, setTime] = useState("30d");

    const fetchData = useCallback(() => {
        axios.get<RarityContract>(`${baseURL}/contracts/${contract_address}`)
        .then((response) => {
            console.log(response)
            setData(response.data)
            setLoaded(true)
        })
    }, [])

    const changeTime = (e:any) => {
        setTime(e.target.value);
        renderData();
    };

    useEffect(() => {
        fetchData()
    }, [])

    const renderData = () => {
        if (loaded && typeof data != "undefined") {
            return (
                <div class={style.collection}>
                    <div>
                        <h1>
                            Collection: <strong>{data['name']}</strong>
                        </h1>
                        {/* <NftImage address={data['address']} tokens={data['tokens']} /> */}
                        <p><strong>Description:</strong></p>
                        <p>{data['description']}</p><br />
                        <p><strong>Tokens:</strong></p>
                        <p>{data['tokens']}</p><br />
                        <p><strong>Unique Owners:</strong></p>
                        <p>{data['unique_owners']}</p>
                    </div>
                    <div>
                        <select value={time} onChange={changeTime}>
                            <option value="24h">24h</option>
                            <option value="7d">7d</option>
                            <option value="30d">30d</option>
                            <option value="all_time">All Time</option>
                        </select>
                        <PriceGraph address={data['id']} time={time} />
                    </div>
                </div>
            );
        }
        return <h2>Loading</h2>
    };

    return renderData();
}

export default Collection;
