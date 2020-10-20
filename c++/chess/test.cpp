/* You can put any private test cases into this file. It will *not* be part of
 * the submission. */

#include "notation.hpp"
#include <cassert>
#include <iostream>

void basic_tests() {
    display_game("e2e4 e7e5\nNg1f3 Nb8c6\nBf1b5 a7a6");
    bool caught = false;
    try {
        display_game("e2e4 Qe7e5");
    } catch (inconsistent_move &m) {
        assert(m.move == "Qe7e5");
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("e2e4 e7e5\nNg1f3 Nb8c6\nBf1b5 a7a6\nb5c6 -");
    } catch (inconsistent_move &m) {
        assert(m.move == "b5c6");
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("e2e4 e7xe5");
    } catch (inconsistent_move &m) {
        assert(m.move == "e7xe5");
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("e2e4 e7e5+");
    } catch (inconsistent_move &m) {
        assert(m.move == "e7e5+");
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("e2e4 d7d5\nf1b5 -");
    } catch (inconsistent_move &m) {
        assert(m.move == "f1b5");
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("e2e4 d7d5Q");
    } catch (inconsistent_move &m) {
        assert(m.move == "d7d5Q");
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("Qa1a2Q+ -");
    } catch (inconsistent_move &m) {
        assert(m.move == "Qa1a2Q+");
        caught = true;
    }
    assert(caught);

    /** This is incomplete notation, and does not fit spec.txt **/
//    caught = false;
//    try {
//        display_game("a2a4 ");
//    } catch (inconsistent_move &m) {
//        caught = true;
//    }
//    assert(caught);
//    caught = false;
//    try {
//        display_game("a2a4");
//    } catch (inconsistent_move &m) {
//        caught = true;
//    }
//    assert(caught);

    std::cout << "Basic tests passed" << std::endl;
}

void sanity() {
    bool caught = false;
    display_game("g2g4 g7g5\nBf1g2 Bf8h6\nNg1f3 Ng8f6\n0-0 0-0");
    try {
        display_game("c2c4 c7c5\n" "a2a3 Nb8c6\n" "g2g3 Bf1h3");
    } catch (bad_piece &m) {
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("a2a4 a7a6\n" "Ra1a2 a8a7");
    } catch (inconsistent_move &m) {
        assert(m.move == "a8a7");
        caught = true;
    }
    assert(caught);
    display_game("g2g4 h7h6\nNb1c3 h6h5\ng4xh5 Rh8xh5\nb2b4 d7d5\nBc1a3 Qd8d7\nBf1h3 Ng8h6\nBh3xd7+ Ke8xd7");

    /** subtest castling **/
    std::string game = "g2g4 g7g5\nBf1g2 Bf8h6\nNg1f3 Ng8f6\n0-0 0-0";
    auto get = display_game(game);
    auto subst = get[0].substr(0, 71);
    assert(subst == "RNBQKBNR\n"
                    "PPPPPPPP\n"
                    " . . . .\n"
                    ". . . . \n"
                    " . . . .\n"
                    ". . . . \n"
                    "pppppppp\n"
                    "rnbqkbnr");

    /** subtest exceptions **/
    caught = false;
    try {
        display_game( "a3a4 a2a3" );
    } catch (no_piece &) {
        caught = true;
    }
    assert(caught);

    /** subtest inconsistent **/
    caught = false;
    try {
        display_game( "a2a4 a7a5\n" "b2b4 a5xb4\n" "a4a5 Ra8a6\n" "Nb1c3 Ra6c6\n" "a5a6 b4xc3\n" "a6a7 b7b6\n" "a7a8 c3xd2+" );
    } catch (inconsistent_move & im) {
        assert(im.move == "a7a8");
        caught = true;
    }
    assert(caught);

    /** subtest legal **/
    std::string game2 = "g2g4 h7h6\n"
                        "Nb1c3 h6h5\n"
                        "g4xh5 Rh8xh5\n"
                        "b2b4 d7d5\n"
                        "Bc1a3 Qd8d7\n"
                        "Bf1h3 Ng8h6\n"
                        "Bh3xd7+ Ke8xd7";

    display_game(game2);

    std::string game3 = "g2g4 h7h6\n"
                        "Nb1c3 h6h5\n"
                        "g4xh5 Rh8xh5\n"
                        "b2b4 d7d5\n"
                        "Bc1a3 Qd8d7\n"
                        "Bf1h3 Ng8h6\n"
                        "Bh3xd7+ Ke8xd7\n";

    display_game(game3);

    std::cout << "Sanity tests passed" << std::endl;
}

void wrong_castling(){
    bool caught = false;
    try {
        display_game("e2e4 e7e5\nBf1d3 Bf8d6\nNg1f3 Ng8f6\nKe1e2 Ke8e7\nQd1e1 Qd8e8\n0-0 0-0");
    } catch (inconsistent_move &m) {
        assert(m.move == "0-0");
        caught = true;
    }
    assert(caught);
    std::cout << "Wrong castling passed" << std::endl;
}

void basic_nicol_test() {
    std::string game = "c2c4 e7e5\n"
                       "Nb1a3 Ng8f6\n"
                       "d2d4 e5xd4\n"
                       "Ng1f3 Bf8xa3\n"
                       "b2xa3 Nb8a6\n"
                       "Nf3xd4 0-0\n"
                       "e2e4 h7h5\n"
                       "c4c5 Na6xc5\n"
                       "a3a4 Nc5xe4\n"
                       "h2h4 Nf6h7\n"
                       "f2f4 g7g5\n"
                       "a2a3 g5xh4\n"
                       "a4a5 f7f5\n"
                       "Nd4xf5 Rf8xf5\n"
                       "a3a4 Rf5xf4\n"
                       "Rh1xh4 Rf4f7\n"
                       "Bf1c4 ";
    display_game(game + '-');

    bool caught = false;
    try {
        display_game(game + "Rf7f1");
    } catch (would_check &) {
        caught = true;
    }
    assert(caught);

    std::string game2 = game + "Ne4g5\nKe1d2 Rf7f2";
    caught = false;
    try {
        display_game(game2);
    } catch (would_check &) {
        caught = true;
    }
    assert(caught);

    std::cout << "Nicol tests passed" << std::endl;
}

void full_game_nicol()
{
    std::string game3 = "c2c4 e7e5\n"
                        "c4c5 d7d5\n"
                        "c5xd6 c7xd6\n"
                        "Nb1a3 b7b5\n"
                        "Na3xb5 Nb8d7\n"
                        "Nb5xa7 Nd7c5\n"
                        "d2d4 Ng8h6\n"
                        "b2b4 e5xd4\n"
                        "Bc1f4 g7g5\n"
                        "Qd1xd4 g5xf4\n"
                        "0-0-0 Nc5a4\n"
                        "g2g4 Nh6f5\n"
                        "g4g5 Nf5xd4\n"
                        "Na7xc8 f7f5\n"
                        "g5xf6 Ra8xc8+\n"
                        "Kc1d2 Rc8c2+\n"
                        "Kd2d3 Na4c5+\n"
                        "Kd3xd4 Qd8xf6+\n"
                        "Kd4d5 Qf6d4+\n"
                        "Kd5c6 Qd4d5+\n"
                        "Kc6b5 Rc2xa2\n"
                        "Rd1xd5 h7h5\n"
                        "Rd5xc5 Ra2a6\n"
                        "Kb5xa6 d6xc5\n"
                        "Ka6b7 c5xb4\n"
                        "e2e4 f4xe3\n"
                        "f2f4 h5h4\n"
                        "h2h3 b4b3\n"
                        "Bf1b5+ Ke8e7\n"
                        "Kb7c7 Rh8h7\n"
                        "Ng1f3 e3e2\n"
                        "Nf3xh4 Ke7f6+\n"
                        "Bb5d7 Bf8c5\n"
                        "Kc7c6 b3b2\n"
                        "Nh4f3 Rh7xh3\n"
                        "Rh1xh3 b2b1Q\n"
                        "Nf3h4 Qb1a2\n"
                        "f4f5 Qa2a6+\n"
                        "Kc6xc5 Qa6b7\n"
                        "Nh4g2 Qb7xd7\n"
                        "Ng2e3 e2e1Q\n"
                        "Ne3d5+ Kf6xf5\n"
                        "Rh3f3+ Kf5e4\n"
                        "Rf3c3 Qe1xc3+\n"
                        "Kc5b6 Qd7c8\n"
                        "Nd5xc3+ Ke4f5\n"
                        "Nc3d5 Qc8e6+\n"
                        "Kb6c5 Qe6xd5+\n"
                        "Kc5xd5 -";

    auto vec = display_game(game3);

    std::cout << "Spicy Nicol tests passed" << std::endl;
}

void en_passant_test() {
    auto game = "e2e4 d7d5\n"
                "e4xd5 c7c5\n"
                "b2b4 e7e5\n"
                "d5xe6 Ke8e7\n"
                "f2f4 Ke7f6\n"
                "Qd1e2 g7g5\n"
                "Qe2f2 g5xf4\n"
                "g2g4 f4xg3";

    auto caught = false;
    try {
        display_game(game);
    } catch (would_check &) {
        caught = true;
    }
    assert(caught);

    std::cout << "En passant test passed" << std::endl;
}

void castling_errors_test() {
    std::string game = "Ng1h3 e7e5\n"
                       "e2e4 Bf8b4\n"
                       "Bf1a6 Bb4xd2+\n"
                       "Ke1e2 ";

    bool caught = false;
    try {
        display_game(game + "Bd2e1\n0-0 0-0");
    } catch (bad_piece &) {
        caught = true;
    }
    assert(caught);

    caught = false;
    try {
        display_game(game + "Ng8h6\n0-0 0-0");
    } catch (no_piece &) {
        caught = true;
    }
    assert(caught);

    caught = false;
    try {
        display_game(game + "0-0");
    } catch (blocked &) {
        caught = true;
    }
    assert(caught);

    std::cout << "Castling errors test passed" << std::endl;
}

void promote_to_king() {
    /** Make sure promotion to king is accepted but is not legal **/

    std::string game = "a2a4 b7b5\n"
                       "a4xb5 a7a6\n"
                       "b5xa6 Nb8c6\n"
                       "a6a7 Ra8b8\n"
                       "a7a8K -\n";

    bool caught = false;
    try {
        display_game(game);
    }
    catch (inconsistent_move &m) {
        caught = m.move == "a7a8K";
    }
    catch (bad_promote &) {
        caught = true;
    }
    assert(caught);

    std::cout << "Non-deterministic promote to king passed" << std::endl;
}

void jirik_sanity() {
    display_game("g2g4 g7g5\nBf1g2 Bf8h6\nNg1f3 Ng8f6\n0-0 0-0");
    bool caught = false;
    try {
        display_game("a7a6 a2a4");
    } catch (bad_piece &) {
        caught = true;
    }
    assert(caught);
    caught = false;
    try {
        display_game("Ba2a4 a2a4");
    } catch (inconsistent_move &) {
        caught = true;
    }
    assert(caught);
    display_game("g2g4 h7h6\nNb1c3 h6h5\ng4xh5 Rh8xh5\nb2b4 d7d5\nBc1a3 Qd8d7\nBf1h3 Ng8h6\nBh3xd7+ Ke8xd7");

    std::cout << "Jirikove failnute sanity passed";
}

int main() {
    basic_tests();
    wrong_castling();
    castling_errors_test();
    en_passant_test();
    promote_to_king();
    basic_nicol_test();
    full_game_nicol();
    sanity();
    jirik_sanity();
}
