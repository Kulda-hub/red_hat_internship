
#include <algorithm>
#include <iostream>
#include "chess.hpp"

/* You may implement methods here. */

bool chess::play(position from, position to, piece promote) {
    auto current_piece = at(from);
    player opponent;
    if (!current_piece.has_value()) throw no_piece();
    if (current_piece->player != current) throw bad_piece();
    if (check_range(to)) throw bad_move();
    lastMove.lapsed = false;
    lastMove.destroyed = false;
    lastMove.en_passanted = false;
    if (current == player::white) {
        opponent = player::black;
    } else{
        opponent = player::white;
    }
    bool is_chequed = in_cheque(locate_king(current), opponent);
    if (from == to) throw bad_move();
    switch (current_piece->piece) {
        case piece::pawn:
            if (current == player::white) {
                pawn_move_white(from,to);
            } else {
                pawn_move_black(from,to);
            }
            break;
        case piece::knight:
            knight_move(from, to, current);
            break;
        case piece::bishop:
            bishop_move(from, to, current);
            break;
        case piece::rook:
            rook_move(from, to, current);
            break;
        case piece::queen:
            queen_move(from,to,current);
            break;
        case piece::king:
            king_move(from,to,current);
            break;
    }
    if (in_cheque(locate_king(current), opponent)) {
        rewind_last_move();
        if (is_chequed) throw in_check();
        throw would_check();
    }
    promote_piece(to, promote);
    if (from == position(1,1) || to == position(1,1)) castleThings.white_left_rook = true;
    if (from == position(8,1) || to == position(8,1)) castleThings.black_left_rook = true;
    if (from == position(1,8) || to == position(1,8)) castleThings.white_right_rook = true;
    if (from == position(8,8) || to == position(8,8)) castleThings.black_right_rook = true;
    if (from.rank == 1 && from.file == 5) castleThings.white_king = true;
    if (from.rank == 8 && from.file == 5) castleThings.black_king = true;
    if (current == player::black) {
        current = player::white;
    } else {
        current = player::black;
    }
    if (current_piece->piece != piece::pawn) {
        en_Passant.is_possible = false;
    }
    return lastMove.destroyed;
}

std::optional <occupant> chess::at(position x) const {
    if (board.find(x) != board.end()) {
        return board.at(x);
    }
    return {};
}

bool chess::pawn_move_white(position from, position to) {
    if (from.file == to.file && from.rank + 1 == to.rank) { //check forward move of 1
        if (!at(to)){
            if (en_Passant.is_possible) set_en_passant_lapsed();
            move_piece(from, to);
            position behind = {from.rank -1, from.file,};
            if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), behind) != en_Passant.lapsed.end()) {
                remove_from_lapsed(behind);
                return true;
            }
            position top_right = {from.rank + 1, from.file + 1};
            position top_left = {from.rank +1, from.file -1};
            if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), top_right) != en_Passant.lapsed.end()) {
                auto two_right = at({from.rank, from.file + 2});
                if (!two_right){
                    remove_from_lapsed(top_right);
                    return true;
                }
                if (two_right->player == player::white && two_right->piece == piece::pawn) return true;
                remove_from_lapsed(top_right);
                return true;
            }
            if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), top_left) != en_Passant.lapsed.end()) {
                auto two_left = at({from.rank, from.file - 2});
                if (!two_left){
                    remove_from_lapsed(top_left);
                    return true;
                }
                if (two_left->player == player::white && two_left->piece == piece::pawn) return true;
                remove_from_lapsed(top_left);
                return true;
            }
            return true;
        }
        throw blocked();
    }

    if ((from.file + 1 == to.file && from.rank + 1 == to.rank)
    || (from.file - 1 == to.file && from.rank + 1 == to.rank)) {  //check taking right and left
        if (at(to).has_value() && at(to)->player == player::black){
            move_piece(from, to);
            return true;
        }
        if (en_Passant.is_possible && to == en_Passant.pos) {
            move_piece(from, to);
            lastMove.destroyed = true;
            lastMove.removed = *at({to.rank - 1, to.file, });
            lastMove.en_passanted = true;
            lastMove.en_passant = {to.rank - 1, to.file, };
            remove_piece({to.rank - 1, to.file, });
            en_Passant.is_possible = false;
            return true;
        }
        if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), to) != en_Passant.lapsed.end()){
            throw lapsed();
        }
        throw bad_move();
    }

    if (from.file == to.file && from.rank == 2 && to.rank == 4) { // check move by two on rank 2
        position extra{
                3, //rank
                from.file, //file
        };
        if (at(to) || at(extra)) throw blocked();
        position left{
                4, //rank
                from.file - 1, //file
        };
        position right{
                4, //rank
                from.file + 1, //file
        };
        if ((at(left)->piece == piece::pawn && at(left)->player == player::black)
        || (at(right)->piece == piece::pawn && at(right)->player == player::black)) {
            en_Passant.is_possible = true;
            en_Passant.pos = extra;
            en_Passant.occupant = {
                    player::white,
                    piece::pawn,
            };
        }
        move_piece(from, to);
        return true;
    }
    throw bad_move();
}

bool chess::pawn_move_black(position from, position to) {
    if (from.file == to.file && from.rank - 1 == to.rank) { //check forward move of 1
        if (!at(to)){
            if (en_Passant.is_possible) set_en_passant_lapsed();
            move_piece(from, to);
            position behind = {from.rank + 1, from.file,};
            if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), behind) != en_Passant.lapsed.end()) {
                remove_from_lapsed(behind);
                return true;
            }
            position bot_right = {from.rank - 1, from.file + 1};
            position bot_left = {from.rank - 1, from.file -1};
            if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), bot_right) != en_Passant.lapsed.end()) {
                auto two_right = at({from.rank, from.file + 2});
                if (!two_right){
                    remove_from_lapsed(bot_right);
                    return true;
                }
                if (two_right->player == player::black && two_right->piece == piece::pawn) return true;
                remove_from_lapsed(bot_right);
                return true;
            }
            if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), bot_left) != en_Passant.lapsed.end()) {
                auto two_left = at({from.rank, from.file - 2});
                if (!two_left){
                    remove_from_lapsed(bot_left);
                    return true;
                }
                if (two_left->player == player::black && two_left->piece == piece::pawn) return true;
                remove_from_lapsed(bot_left);
                return true;
            }
            return true;
        }
        throw blocked();
    }

    if ((from.file + 1 == to.file && from.rank - 1 == to.rank)
        || (from.file - 1 == to.file && from.rank - 1 == to.rank)) {  //check taking right and left
        if (at(to).has_value() && at(to)->player == player::white){
            move_piece(from, to);
            return true;
        }
        if (en_Passant.is_possible && to == en_Passant.pos) {
            move_piece(from, to);
            lastMove.destroyed = true;
            lastMove.removed = *at({to.rank + 1, to.file, });
            lastMove.en_passanted = true;
            lastMove.en_passant = {to.rank + 1, to.file, };
            remove_piece({to.rank + 1, to.file, });
            en_Passant.is_possible = false;
            return true;
        }
        if (std::find(en_Passant.lapsed.begin(), en_Passant.lapsed.end(), to) != en_Passant.lapsed.end()){
            throw lapsed();
        }
        throw bad_move();
    }

    if (from.file == to.file && from.rank == 7 && to.rank == 5) { // check move by two on rank 2
        position extra{
                6, //rank
                from.file, //file
        };
        if (at(to) || at(extra)) throw blocked();
        position left{
                5, //rank
                from.file - 1, //file
        };
        position right{
                5, //rank
                from.file + 1, //file
        };
        if ((at(left)->piece == piece::pawn && at(left)->player == player::white)
            || (at(right)->piece == piece::pawn && at(right)->player == player::white)) {
            en_Passant.is_possible = true;
            en_Passant.pos = extra;
            en_Passant.occupant = {
                    player::black,
                    piece::pawn,
            };
        }
        move_piece(from,to);
        return true;
    }
    throw bad_move();
}

bool chess::knight_move(position from, position to, player current_player){
    int ranks[] = {2, 2, -2,-2, 1, 1, -1, -1};
    int files[] = {1, -1, 1,-1, 2, -2, 2, -2};
    for (int i = 0; i < 8; ++i) {
        position current_pos = {from.rank + ranks[i],
                            from.file + files[i],};
        if (current_pos == to) {
            if (!at(to)){
                move_piece(from, to);
                return true;
            }
            if (at(to)->player != current_player){
                move_piece(from, to);
                return true;
            }
            throw blocked();
        }
    }
    throw bad_move();
}

bool chess::bishop_move(position from, position to, player current_player){
    int top = -1;
    int right = -1;
    if ( to.rank == from.rank || to.file == from.file ) throw bad_move();
    if ( to.rank > from.rank ) top = 1;
    if ( to.file > from.file ) right = 1;
    position current_pos = {from.rank + top, from.file + right};
    while (current_pos != to) {
        if (at(current_pos)) throw blocked();
        current_pos.rank += top;
        current_pos.file += right;
    }
    if (!at(to)) {
        move_piece(from, to);
        return true;
    }
    if (at(to)->player != current_player) {
        move_piece(from, to);
        return true;
    }
    throw blocked();
}

bool chess::rook_move(position from, position to, player current_player){
    if ( to.rank != from.rank && to.file != from.file ) throw bad_move();
    int top = 0;
    int right = 0;
    if ( to.rank == from.rank ){
        to.file > from.file ? right = 1 : right = -1;
    }
    if ( to.file == from.file ){
        to.rank > from.rank ? top = 1 : top = -1;
    }
    position current_pos = {from.rank + top, from.file + right};
    while (current_pos != to) {
        if (at(current_pos)) throw blocked();
        current_pos.rank += top;
        current_pos.file += right;
    }
    if (!at(to)) {
        move_piece(from, to);
        return true;
    }
    if (at(to)->player != current_player) {
        move_piece(from, to);
        return true;
    }
    throw blocked();



}

bool chess::queen_move(position from, position to, player current_player){
    int top = 0;
    int right = 0;
    if ( to.rank != from.rank && to.file != from.file && std::abs(to.rank - from.rank) != std::abs(to.file - from.file)) throw bad_move();
    if ( to.rank > from.rank ) top = 1;
    if ( to.rank < from.rank ) top = -1;
    if ( to.file > from.file ) right = 1;
    if ( to.file < from.file ) right = -1;
    position current_pos = {from.rank + top, from.file + right};
    while (current_pos != to) {
        if (at(current_pos)) throw blocked();
        current_pos.rank += top;
        current_pos.file += right;
    }
    if (!at(to)) {
        move_piece(from, to);
        return true;
    }
    if (at(to)->player != current_player) {
        move_piece(from, to);
        return true;
    }
    throw blocked();
}

bool chess::king_move(position from, position to, player current_player){
    if (current_player == player::white) {
        position start_pos = {1,5};
        position left_castle = {1,3};
        position right_castle = {1,7};
        if (from == start_pos && to == left_castle) {
            check_white_left_castle();
            move_piece(from,to);
            move_piece({1,1}, {1,4});
            castleThings.white_king = true;
            return true;
        }
        if (from == start_pos && to == right_castle) {
            check_white_right_castle();
            move_piece(from,to);
            move_piece({1,8}, {1,6});
            castleThings.white_king = true;
            return true;
        }
    }
    if (current_player == player::black) {
        position start_pos = {8,5};
        position left_castle = {8,3};
        position right_castle = {8,7};
        if (from == start_pos && to == left_castle) {
            check_black_left_castle();
            move_piece(from,to);
            move_piece({8,1}, {8,4});
            castleThings.black_king = true;
            return true;
        }
        if (from == start_pos && to == right_castle) {
            check_black_right_castle();
            move_piece(from,to);
            move_piece({8,8}, {8,6});
            castleThings.black_king = true;
            return true;
        }
    }

    if (abs(to.rank - from.rank) > 1 || abs(to.file - from.file) > 1) throw bad_move();
    auto target = at(to);
    if (target.has_value() && target->player == current_player) throw blocked();
    move_piece(from, to);
    if (current_player == player::white) {
        castleThings.white_king = true;
    } else {
        castleThings.black_king = true;
    }
    return true;
}
bool chess::in_cheque(position current_pos, player opposing_player){
    int ranks_knight[] = {2, 2, -2, -2, 1, 1, -1, -1}; //knight combinations
    int files_kinght[] = {1, -1, 1, -1, 2, -2, 2, -2};
    for (int i = 0; i < 8; ++i) { // check for knight cheques
        auto piece = at({current_pos.rank + ranks_knight[i], current_pos.file + files_kinght[i]});
        if (piece.has_value() && piece->piece == piece::knight && piece->player == opposing_player) return true;
    }
    int ranks_straight[] = {1,0,-1,0};
    int files_straight[] = {0,1,0,-1};
    for (int j = 0; j < 4; ++j) { //check straight lines
        for (int i = 1; i < 8; ++i) {
            auto piece = at({current_pos.rank + ranks_straight[j]*i, current_pos.file + files_straight[j]*i});
            if (!piece.has_value()) continue;
            if (piece.has_value() && piece->player == opposing_player &&
            (piece->piece == piece::queen || piece->piece == piece::rook)) return true;
            break;
        }
    }
    int ranks_slant[] = {1,1,-1,-1};
    int files_slant[] = {-1,1,1,-1};
    for (int k = 0; k < 4; ++k) { //check slant lines
        for (int i = 1; i < 8; ++i) {
            auto piece = at({current_pos.rank + ranks_slant[k]*i, current_pos.file + files_slant[k]*i});
            if (!piece.has_value()) continue;
            if (piece.has_value() && piece->player == opposing_player &&
                (piece->piece == piece::queen || piece->piece == piece::bishop)) return true;
            break;
        }
    }
    if (opposing_player == player::black) {
        auto pawn1 = at({current_pos.rank + 1, current_pos.file - 1,});
        auto pawn2 = at({current_pos.rank + 1, current_pos.file + 1,});
        if (pawn1.has_value() && pawn1->player == player::black && pawn1->piece == piece::pawn) return true;
        if (pawn2.has_value() && pawn2->player == player::black && pawn2->piece == piece::pawn) return true;
    }
    if (opposing_player == player::white) {
        auto pawn1 = at({current_pos.rank - 1, current_pos.file - 1,});
        auto pawn2 = at({current_pos.rank - 1, current_pos.file + 1,});
        if (pawn1.has_value() && pawn1->player == player::white && pawn1->piece == piece::pawn) return true;
        if (pawn2.has_value() && pawn2->player == player::white && pawn2->piece == piece::pawn) return true;
    }
    return false;
}

bool chess::check_range(position to) {
    return to.file > 8 || to.rank > 8 || to.file < 1 || to.rank < 1;
}

void chess::move_piece(position from, position to) {
    lastMove.destroyed = false;
    lastMove.from = from;
    lastMove.to = to;
    if (at(to)){
        lastMove.destroyed = true;
        lastMove.removed = *at(to);
        remove_piece(to);
    }
    occupant piece_to_move = *at(from);
    board.insert({to, piece_to_move});
    remove_piece(from);
}

void chess::rewind_last_move(){
    occupant piece_to_move = *at(lastMove.to);
    board.insert({lastMove.from, piece_to_move});
    remove_piece(lastMove.to);
    if (lastMove.destroyed){
        if (lastMove.en_passanted) {
            board.insert({lastMove.en_passant, lastMove.removed});
            lastMove.en_passanted = false;
        } else {
            board.insert({lastMove.to, lastMove.removed});
        }
    }
    if (lastMove.lapsed) {
        en_Passant.lapsed.push_back(lastMove.lapsed_pos);
        lastMove.lapsed = false;
    }
    lastMove.destroyed = false;
}

void chess::remove_from_lapsed(position x) {
    en_Passant.lapsed.erase(std::remove(en_Passant.lapsed.begin(),
                                        en_Passant.lapsed.end(), x), en_Passant.lapsed.end());
    lastMove.lapsed = true;
    lastMove.lapsed_pos = x;
}

void chess::set_en_passant_lapsed() {
    if (en_Passant.is_possible) en_Passant.lapsed.push_back(en_Passant.pos);
    en_Passant.is_possible = false;
}

void chess::check_white_left_castle(){
    auto left_rook = at({1,1});
    if (!(left_rook.has_value() && left_rook->piece == piece::rook && left_rook->player == player::white)){
        throw bad_move();
    }
    if (at({1,2}) || at({1,3}) || at({1,4})) throw blocked();
    if (in_cheque({1,5}, player::black)) throw in_check();
    if (in_cheque({1,3}, player::black)) throw would_check();
    if (in_cheque({1,4}, player::black)) throw would_check();
    if (castleThings.white_left_rook || castleThings.white_king) throw has_moved();
}

void chess::check_white_right_castle() {
    auto right_rook = at({1, 8});
    if (!(right_rook.has_value() && right_rook->piece == piece::rook && right_rook->player == player::white)){
        throw bad_move();
    }
    if (at({1,6}) || at({1,7})) throw blocked();
    if (in_cheque({1,5}, player::black)) throw in_check();
    if (in_cheque({1,6}, player::black)) throw would_check();
    if (in_cheque({1,7}, player::black)) throw would_check();
    if (castleThings.white_right_rook || castleThings.white_king) throw has_moved();
}

void chess::check_black_left_castle() {
    auto left_rook = at({8,1});
    if (!(left_rook.has_value() && left_rook->piece == piece::rook && left_rook->player == player::black)){
        throw bad_move();
    }
    if (at({8,2}) || at({8,3}) || at({8,4})) throw blocked();
    if (in_cheque({1,5}, player::white)) throw in_check();
    if (in_cheque({1,3}, player::white)) throw would_check();
    if (in_cheque({1,4}, player::white)) throw would_check();
    if (castleThings.black_left_rook || castleThings.black_king) throw has_moved();
}

void chess::check_black_right_castle() {
    auto right_rook = at({8, 8});
    if (!(right_rook.has_value() && right_rook->piece == piece::rook && right_rook->player == player::black)){
        throw bad_move();
    }
    if (at({8,6}) || at({8,7})) throw blocked();
    if (in_cheque({8,5}, player::white)) throw in_check();
    if (in_cheque({8,6}, player::white)) throw would_check();
    if (in_cheque({8,7}, player::white)) throw would_check();
    if (castleThings.black_right_rook || castleThings.black_king) throw has_moved();
}

position chess::locate_king(player color){
    auto it = board.begin();
    while (it != board.end()) {
        if (it->second.piece == piece::king && it->second.player == color) {
            return it->first;
        }
        it++;
    }
    return {0,0};
}

void chess::promote_piece(position x, piece to_promote){
    auto piece = at(x);
    if (piece->piece == piece::pawn ) {
        if (x.rank == 8 && piece->player == player::white) {
            if (to_promote == piece::pawn || to_promote == piece::king){
                rewind_last_move();
                throw bad_promote();
            }
            remove_piece(x);
            board.insert({x,{player::white,to_promote}});
        }
        if (x.rank == 1 && piece->player == player::black) {
            if (to_promote == piece::pawn || to_promote == piece::king){
                rewind_last_move();
                throw bad_promote();
            }
            remove_piece(x);
            board.insert({x,{player::black,to_promote}});
        }
    }
}

chess::chess() {
    lastMove = {{0,0},{0,0},false, {player::black, piece::pawn}};
    current = player::white;
    en_Passant = {{0, 0}, false, {player::black, piece::pawn},{},};
    for (int i = 1; i < 9; ++i) {
        board.insert({{7, i},{player::black, piece::pawn}}); //b pawns initialize
        board.insert({{2, i},{player::white, piece::pawn}}); //w pawns initialize
    }
    board.insert({{1, 1},{player::white, piece::rook}}); //w rook initialize
    board.insert({{1, 2},{player::white, piece::knight}}); //w knight initialize
    board.insert({{1, 3},{player::white, piece::bishop}}); //w bishop initialize
    board.insert({{1, 4},{player::white, piece::queen}}); //w queen initialize
    board.insert({{1, 5},{player::white, piece::king}}); //w king initialize
    board.insert({{1, 6},{player::white, piece::bishop}}); //w bishop initialize
    board.insert({{1, 7},{player::white, piece::knight}}); //w knight initialize
    board.insert({{1, 8},{player::white, piece::rook}}); //w rook initialize

    board.insert({{8, 1},{player::black, piece::rook}}); //b rook initialize
    board.insert({{8, 2},{player::black, piece::knight}}); //b knight initialize
    board.insert({{8, 3},{player::black, piece::bishop}}); //b bishop initialize
    board.insert({{8, 4},{player::black, piece::queen}}); //b queen initialize
    board.insert({{8, 5},{player::black, piece::king}}); //b king initialize
    board.insert({{8, 6},{player::black, piece::bishop}}); //b bishop initialize
    board.insert({{8, 7},{player::black, piece::knight}}); //b knight initialize
    board.insert({{8, 8},{player::black, piece::rook}}); //b rook initialize
}



