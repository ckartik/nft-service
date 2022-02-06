// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

// Gets the contract fomr 
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    // This will denote the number of NFTs minted
    uint256 public tokenCounter;
    constructor () public ERC721 ("Dogie", "DOG"){
        // Used as a way to generate unqiue ID's for each NFT.
        tokenCounter = 0;
    }
    
    // We're assigning a new token id
    function createCollectible(string memory tokenURI) public returns (uint256) {
        uint256 newItemId = tokenCounter;
        // Param 1: Takes a new address for the owner of the NFT.
        // Param 2: Takes the unique id associated with each NFT.
        _safeMint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newItemId;
    }

}
