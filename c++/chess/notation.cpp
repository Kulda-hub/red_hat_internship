/* You can implement display_game in here. */
#include <iostream>
#include "notation.hpp"

void print(chess const &board) {
    bool white = true;
    for (int rank = 8; rank > 0; rank--) {
        for (int file = 1; file < 9; file++) {
            auto occupant = board.at(position(rank, file));
            if (!occupant) {
                if (white) {
                    std::cout << " ";
                } else {
                    std::cout << ".";
                }
                white = !white;
                continue;
            }
            white = !white;
            if (occupant.value().player == player::black) {
                switch (occupant.value().piece) {
                    case piece::pawn:
                        std::cout << "P";
                        break;
                    case piece::rook:
                        std::cout << "R";
                        break;
                    case piece::knight:
                        std::cout << "N";
                        break;
                    case piece::bishop:
                        std::cout << "B";
                        break;
                    case piece::queen:
                        std::cout << "Q";
                        break;
                    default:
                        std::cout << "K";
                        break;
                }
            } else {
                switch (occupant.value().piece) {
                    case piece::pawn:
                        std::cout << "p";
                        break;
                    case piece::rook:
                        std::cout << "r";
                        break;
                    case piece::knight:
                        std::cout << "n";
                        break;
                    case piece::bishop:
                        std::cout << "b";
                        break;
                    case piece::queen:
                        std::cout << "q";
                        break;
                    default:
                        std::cout << "k";
                        break;
                }
            }
        }
        std::cout << std::endl;
        white = !white;
    }
}

std::string make_string(chess const &board) {
    bool white = true;
    std::string returnString;
    for (int rank = 8; rank > 0; rank--) {
        for (int file = 1; file < 9; file++) {
            auto occupant = board.at(position(rank, file));
            if (!occupant) {
                if (white) {
                    returnString += " ";
                } else {
                    returnString += ".";
                }
                white = !white;
                continue;
            }
            white = !white;
            if (occupant.value().player == player::black) {
                switch (occupant.value().piece) {
                    case piece::pawn:
                        returnString += "P";
                        break;
                    case piece::rook:
                        returnString += "R";
                        break;
                    case piece::knight:
                        returnString += "N";
                        break;
                    case piece::bishop:
                        returnString += "B";
                        break;
                    case piece::queen:
                        returnString += "Q";
                        break;
                    default:
                        returnString += "K";
                        break;
                }
            } else {
                switch (occupant.value().piece) {
                    case piece::pawn:
                        returnString += "p";
                        break;
                    case piece::rook:
                        returnString += "r";
                        break;
                    case piece::knight:
                        returnString += "n";
                        break;
                    case piece::bishop:
                        returnString += "b";
                        break;
                    case piece::queen:
                        returnString += "q";
                        break;
                    default:
                        returnString += "k";
                        break;
                }
            }
        }
        returnString += "\n";
        white = !white;
    }
    return returnString;
}

//from stackoverflow
std::vector<std::string> split (std::string s, std::string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    std::string token;
    std::vector<std::string> res;

    while ((pos_end = s.find (delimiter, pos_start)) != std::string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}

piece string_to_piece(const std::string& str){
    if (str == "B") return piece::bishop;
    if (str == "K") return piece::king;
    if (str == "Q") return piece::queen;
    if (str == "R") return piece::rook;
    if (str == "N") return piece::knight;
    return piece::pawn;
}

position strings_to_position(const std::string &strfile, const std::string &strrank){
    position returnpos = {1,1};
    if (strfile == "b") returnpos.file = 2;
    if (strfile == "c") returnpos.file = 3;
    if (strfile == "d") returnpos.file = 4;
    if (strfile == "e") returnpos.file = 5;
    if (strfile == "f") returnpos.file = 6;
    if (strfile == "g") returnpos.file = 7;
    if (strfile == "h") returnpos.file = 8;
    if (strrank == "2") returnpos.rank = 2;
    if (strrank == "3") returnpos.rank = 3;
    if (strrank == "4") returnpos.rank = 4;
    if (strrank == "5") returnpos.rank = 5;
    if (strrank == "6") returnpos.rank = 6;
    if (strrank == "7") returnpos.rank = 7;
    if (strrank == "8") returnpos.rank = 8;
    return returnpos;

}

void playWhite(chess &chs, std::string str){
    std::regex rgx("(([RKQNB]?)([a-h])([1-8])(x?)([a-h])([1-8])([RQNBK]?)(\\+?)|(0-0)(\\+)?$|(0-0-0)(\\+)?)");
    std::smatch matches;
    std::regex_search(str,matches, rgx);
    position from = {0,0};
    position to = {0,0};
    piece moved = piece::pawn;
    piece promote = piece::pawn;
    bool takes = false;
    bool cheque = false;
    if (matches.str(10) == "0-0") {
        from = {1,5};
        to = {1,7};
        cheque = matches.str(11) == "+";
        auto king = chs.at(from);
        if (king.has_value() && king->player == player::white && king->piece != piece::king){
            throw inconsistent_move(matches.str());
        }
        if (chs.in_cheque(chs.locate_king(player::black), player::white) != cheque) {
            throw inconsistent_move(matches.str());
        }
        chs.play(from, to, promote);
        return;
    }
    if (matches.str(12) == "0-0-0") {
        from = {1,5};
        to = {1,3};
        cheque = matches.str(13) == "+";
        auto king = chs.at(from);
        if (king.has_value() && king->player == player::white && king->piece != piece::king){
            throw inconsistent_move(matches.str());
        }
        if (chs.in_cheque(chs.locate_king(player::black), player::white) != cheque) {
            throw inconsistent_move(matches.str());
        }
        chs.play(from, to, promote);
        return;
    }
    moved = string_to_piece(matches.str(2));
    from = strings_to_position(matches.str(3), matches.str(4));
    takes = matches.str(5) == "x";
    to = strings_to_position(matches.str(6), matches.str(7));
    promote = string_to_piece(matches.str(8));
    cheque = matches.str(9) == "+";
    auto realPiece = chs.at(from);
    if (realPiece.has_value() && realPiece->piece != moved) {
        throw inconsistent_move(matches.str());
    }
    if (realPiece.has_value() && realPiece->piece == piece::pawn && to.rank == 8 && promote == piece::pawn) {
        throw inconsistent_move(matches.str());
    }
    if ((realPiece.has_value()) && (to.rank != 8 || realPiece->piece != piece::pawn) && (promote != piece::pawn)) {
        throw inconsistent_move(matches.str());
    }
    if (chs.play(from, to, promote) != takes){
        throw inconsistent_move(matches.str());
    }

    if (chs.in_cheque(chs.locate_king(player::black), player::white) != cheque){
        throw inconsistent_move(matches.str());
    }

}

void playBlack(chess &chs, std::string str){
    std::regex rgx("(([RKQNB]?)([a-h])([1-8])(x?)([a-h])([1-8])([RQNBK]?)(\\+?)|(0-0)(\\+)?$|(0-0-0)(\\+)?)");
    std::smatch matches;
    std::regex_search(str,matches, rgx);
    position from = {0,0};
    position to = {0,0};
    piece moved = piece::pawn;
    piece promote = piece::pawn;
    bool takes = false;
    bool cheque = false;
    if (matches.str(10) == "0-0") {
        from = {8,5};
        to = {8,7};
        cheque = matches.str(11) == "+";
        auto king = chs.at(from);
        if (king.has_value() && king->player == player::black && king->piece != piece::king){
            throw inconsistent_move(matches.str());
        }
        if (chs.in_cheque(chs.locate_king(player::white), player::black) != cheque) {
            throw inconsistent_move(matches.str());
        }
        chs.play(from, to, promote);
        return;
    }
    if (matches.str(12) == "0-0-0") {
        from = {8,5};
        to = {8,3};
        cheque = matches.str(13) == "+";
        auto king = chs.at(from);
        if (king.has_value() && king->player == player::black && king->piece != piece::king){
            throw inconsistent_move(matches.str());
        }
        if (chs.in_cheque(chs.locate_king(player::white), player::black) != cheque) {
            throw inconsistent_move(matches.str());
        }
        chs.play(from, to, promote);
        return;
    }
    moved = string_to_piece(matches.str(2));
    from = strings_to_position(matches.str(3), matches.str(4));
    takes = matches.str(5) == "x";
    to = strings_to_position(matches.str(6), matches.str(7));
    promote = string_to_piece(matches.str(8));
    cheque = matches.str(9) == "+";
    auto realPiece = chs.at(from);
    if (realPiece.has_value() && realPiece->piece != moved){
        throw inconsistent_move(matches.str());
    }
    if (realPiece.has_value() && realPiece->piece == piece::pawn && to.rank == 1 && promote == piece::pawn) {
        throw inconsistent_move(matches.str());
    }
    if ((realPiece.has_value()) && (to.rank != 1 || realPiece->piece != piece::pawn) && (promote != piece::pawn)) {
        throw inconsistent_move(matches.str());
    }
    if (chs.play(from, to, promote) != takes){
        throw inconsistent_move(matches.str());
    }

    if (chs.in_cheque(chs.locate_king(player::white), player::black) != cheque){
        throw inconsistent_move(matches.str());
    }
}

std::vector<std::string> display_game(std::string game) {
    chess s;
    std::vector< std::string > splitGame = split(game, "\n");
    std::vector< std::string > returnvec = {};
    returnvec.push_back(make_string(s));
    for (std::string str : splitGame){
        if (str == "") break;
        auto spltstr = split(str, " ");
        playWhite(s, spltstr[0]);
        returnvec.push_back(make_string(s));
        if (spltstr[1] =="-") return returnvec;
        playBlack(s, spltstr[1]);
        returnvec.push_back(make_string(s));
    }
    return returnvec;
}


inconsistent_move::inconsistent_move(const std::string &move) : move(move) {}


