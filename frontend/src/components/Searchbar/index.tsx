import { FunctionalComponent, Component, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";

// import Data from "some backend json file"

interface dataProps {
}

interface dataState {
query: string;
data: String[];
filteredData: String[];
}

// class SearchBar extends Component<dataProps, dataState> {
//     state = {
//       query: "",
//       data: [],
//       filteredData: []
//     };

//     handleInputChange = event => {
//       const query = event.target.value;

//       this.setState(prevState => {
//         const filteredData = prevState.data.filter(element => {
//           return element.name.toLowerCase().includes(query.toLowerCase());
//         });

//         return {
//           query,
//           filteredData
//         };
//       });
//     };

//     getData = () => {
//       fetch(`insert endpoint here`)
//         .then(response => response.json())
//         .then(data => {
//           const { query } = this.state;
//           const filteredData = data.filter(element => {
//             return element.name.toLowerCase().includes(query.toLowerCase());
//           });

//           this.setState({
//             data,
//             filteredData
//           });
//         });
//     };

//     componentWillMount() {
//       this.getData();
//     }

//     render() {
//       return (
//         <div className="searchForm">
//           <form>
//             <input
//               placeholder="Search for NFT.."
//               value={this.state.query}
//               onChange={this.handleInputChange}
//             />
//           </form>
//           <div>{this.state.filteredData.map(i => <p>{i.name}</p>)}</div>
//         </div>
//       );
//     }
//   }

const Searchbar:FunctionalComponent = () => {
  return (
    <div>
      <input type="text"></input>
    </div>
  )
}


export default Searchbar;
