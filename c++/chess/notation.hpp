#include <string>
#include <vector>
#include <regex>
#include "chess.hpp"

/* Convert a game in algebraic notation into a sequence of
 * chessboard snapshots. See spec.txt for details. */

std::vector< std::string > display_game( std::string game );

/* The above function may throw any exceptions defined in chess.hpp.
 * Additionally, throw the following exception with 'move' filled in
 * with the offending string (i.e. a single move that failed) if the
 * move description does not match reality:
*
 *  • the piece on the indicated position does not match (e.g.
 *    'a2a4' in the input, but a2 is occupied by a rook at the time...
 *    set 'move' to 'a2a4' in this case),
 *  • capture was indicated but did not happen (or vice versa:
 *    capture happened but was not indicated),
 *  • check was indicated but did not happen (or vice versa),
 *  • promotion was indicated but did not happen (or vice versa). */

struct inconsistent_move:std::exception
{
    inconsistent_move(const std::string &move);

    std::string move;
};

void print(chess const &board);

/* Except for the above conditions, assume that the input string
 * conforms to the specification. */
