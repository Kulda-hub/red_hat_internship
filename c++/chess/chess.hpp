#include <optional>
#include <map>
#include <vector>

struct position
{
    int rank; /* row number, starting at 1 */
    int file; /* column 'letter', a = 1, b = 2, ... */
public:

    position(int rank, int file) : rank(rank), file(file) {}

    bool operator== (const position &r) const{
        return this->rank == r.rank && this->file == r.file;
    }
    bool operator!= (const position &r) const{
        return !(*this == r);
    }
    bool operator< (const position &r) const{
        if (this->rank != r.rank) return this->rank < r.rank;
        return this->file < r.file;
    }
};

enum class piece  { pawn, rook, knight, bishop, queen, king };
enum class player { white, black };

struct occupant
{
    ::player player;
    ::piece piece;
};

struct en_passant //contains info about possible en-passant
{
    position pos = position(0,0);
    bool is_possible;
    ::occupant occupant;
    std::vector< position > lapsed;
};

struct castle_things //contains info if pieces needed for castling moved
{
    bool white_left_rook = false;
    bool white_right_rook = false;
    bool white_king = false;
    bool black_left_rook = false;
    bool black_right_rook = false;
    bool black_king = false;
};

struct last_move
{
    position from = position(0,0);
    position to = position(0,0);
    bool destroyed = false;
    occupant removed = {player::black, piece::pawn};
    bool en_passanted = false;
    position en_passant = position(0,0);
    bool lapsed = false;
    position lapsed_pos = position(0,0);
};


class chess
{
    std::map<position, occupant> board;
    player current;
    en_passant en_Passant;
    castle_things castleThings;
    last_move lastMove;

public:
    chess();

    /* Move a piece currently at ‹from› to square ‹to›:
     *
     * • in case the move places a pawn at its 8th rank (rank 8 for
     *   white, rank 1 for black), it is promoted to the piece given
     *   in ‹promote_piece› (otherwise, the last argument is ignored),
     * • throws exceptions (see below) if the move is illegal,
     * • castling is described as a king move of more than one square,
     * • returns ‹true› when the move has resulted in a capture,
     * • if an exception is thrown, ‹play› may be called again for
     *   the same player. */

    bool play( position from, position to, piece promote );

    /* Which piece (if any) is at the given position? */
    std::optional< occupant > at( position x) const;

    bool pawn_move_white(position from, position to);

    bool check_range(position to);

    void remove_piece(position x){board.erase(x);};

    void move_piece(position from, position to);

    void remove_from_lapsed(position x);

    void set_en_passant_lapsed();

    bool pawn_move_black(position from, position to);

    bool knight_move(position from, position to, player current_player);

    bool bishop_move(position from, position to, player current_player);

    bool rook_move(position from, position to, player current_player);

    bool queen_move(position from, position to, player current_player);

    bool in_cheque(position current_pos, player opposing_player);

    void rewind_last_move();

    position locate_king(player color);

    bool king_move(position from, position to, player current_player);

    void check_white_left_castle();

    void check_white_right_castle();

    void check_black_left_castle();

    void check_black_right_castle();

    void promote_piece(position x, piece to_promote);

    void printerino();
};

/* The following are exceptions to be thrown by ‹play› if the move
 * is illegal. The classes are shown in the order of precedence: the
 * first applicable should be thrown. Attempting an «en passant»
 * when the pieces are in the wrong place is a ‹bad_move›. */

struct no_piece:std::exception{};    /* there is no piece on the ‹from› square */
struct bad_piece:std::exception{};   /* the piece on ‹from› is not ours */
struct bad_move:std::exception{};    /* this move is not available for this piece */
struct blocked:std::exception{};     /* another piece is in the way */
struct lapsed:std::exception{};      /* «en passant» capture is no longer allowed */
struct in_check:std::exception{};    /* the player is currently in check and the
                       move does not get them out */
struct would_check:std::exception{}; /* the move would place the player in check */
struct has_moved:std::exception{};   /* one of the castling pieces has already moved */
struct bad_promote:std::exception{}; /* promotion to a pawn or king was attempted */

/* In addition to ‹has_moved›, (otherwise legal) castling may throw:
 *  • ‹blocked› -- some pieces are in the way
 *  • ‹in_check› -- the king is currently in check
 *  • ‹would_check› -- would pass through or end up in check */
