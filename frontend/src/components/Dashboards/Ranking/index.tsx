import { FunctionalComponent, h } from "preact";
import { useState } from "preact/hooks";

const Ranking: FunctionalComponent = () => {
    const [rankValue, setRankValue] = useState("min_price");
    const [data, setData] = useState({});

    const changeRank = (e:any) => {
        setRankValue(e.target.value);
    }

    //////////////WIP///////////////
    // let fetchData = useCallback(() => {
    //     fetch("google.com")
    //     .then((response) => {
    //         setData(response)
    //     })
    // }, [rankValue])

    // useEffect(() => {
    //     fetchData;
    // },[rankValue])

    const renderTable = (value:string) => {
        if (value == "trending") {
            return renderTrending();
        }
        return renderTop();
    }

    const renderTrending = () => {
        const headers = ["Collection", "Collection Name", "Total Volume", "Percent Change"];
        return (
            <table>
                <thead>
                    <tr>{headers.map((header) => <th class="header">{header}</th>)}</tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
        );
    }

    const renderTop = () => {
        const values:{[k:string]:string} = {"min_price": "Minimum Sale Value",
                                            "max_price": "Maximum Sale Value",
                                            "volume":    "Total Volume"       };
        const headers = ["Collection", "Collection Name", values[rankValue]];
        return (
            <table>
                <thead>
                    <tr>{headers.map((header) => <th class="header">{header}</th>)}</tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
        );
    }




    return(
        <div>
            <h1>This is the Ranking Component.</h1>
            <select value={rankValue} onChange={changeRank}>
                <option value="min_price">Min Price</option>
                <option value="max_price">Max Price</option>
                <option value="volume">Volume</option>
                <option value="trending">Trending</option>
            </select>
            {renderTable(rankValue)}
            {/*///////////////WIP///////////////////////*/}
            {/* <button onClick={fetchData}>{rankValue}</button>
            <code>{data}</code> */}
        </div>
    );
}

export default Ranking;
