#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <winsock2.h>
#include <pthread.h>

#define PORTA 5000

typedef struct {
    int vez;
    int lista;
    int achado[10];
    int pontos[3];
    int passou;
    int fim;
    char nome[3][30];
} jogo;

jogo j;
pthread_mutex_t trava = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t sinal = PTHREAD_COND_INITIALIZER;
SOCKET sock;
int eu, outro;

char titulos[10][60] = {
    "Os 10 paises mais populosos do mundo",
    "As 10 capitais brasileiras mais populosas",
    "Os 10 super-herois mais populares",
    "Os 10 animes mais famosos no Brasil",
    "Os 10 videogames mais famosos de todos os tempos",
    "Os 10 itens mais famosos do McDonald's",
    "As 10 lendas do folclore brasileiro mais famosas",
    "As 10 redes sociais mais usadas do mundo",
    "Os 10 desenhos animados mais famosos",
    "Os 10 clubes europeus mais famosos"
};

char itens[10][10][60] = {
    {"India", "China", "Estados Unidos|EUA|USA", "Indonesia", "Paquistao", "Nigeria", "Brasil", "Bangladesh", "Russia", "Mexico"},
    {"Sao Paulo|SP|Sampa", "Rio de Janeiro|Rio|RJ", "Brasilia|DF", "Fortaleza", "Salvador", "Belo Horizonte|BH", "Manaus", "Curitiba", "Recife", "Goiania"},
    {"Homem-Aranha", "Batman", "Superman", "Homem de Ferro", "Mulher-Maravilha", "Capitao America", "Hulk", "Thor", "Flash", "Pantera Negra"},
    {"Naruto", "Dragon Ball", "One Piece", "Pokemon", "Cavaleiros do Zodiaco", "Attack on Titan|Shingeki no Kyojin", "Death Note", "Demon Slayer|Kimetsu no Yaiba", "Jujutsu Kaisen", "Fullmetal Alchemist"},
    {"Minecraft", "GTA|Grand Theft Auto", "Super Mario|Mario", "Tetris", "Fortnite", "Pokemon", "FIFA|EA FC", "Call of Duty", "The Sims|Sims", "Pac-Man"},
    {"Big Mac", "McFritas|Batata frita|Batata", "Quarterao", "McChicken", "Cheeseburger", "McNuggets|Nuggets", "McFlurry", "Casquinha", "McLanche Feliz", "Cheddar McMelt"},
    {"Saci-Perere|Saci", "Curupira", "Mula sem Cabeca", "Iara|Mae d'Agua", "Boto-cor-de-rosa|Boto", "Boitata", "Lobisomem", "Cuca", "Caipora", "Negrinho do Pastoreio"},
    {"Facebook", "YouTube", "Instagram", "WhatsApp|Zap", "TikTok", "WeChat", "Telegram", "Messenger", "Snapchat", "X|Twitter"},
    {"Os Simpsons|Simpsons", "Bob Esponja", "Tom e Jerry", "Pica-Pau", "Scooby-Doo", "Os Flintstones|Flintstones", "Looney Tunes|Pernalonga", "Meninas Superpoderosas", "Dragon Ball", "Hora de Aventura"},
    {"Real Madrid", "Barcelona|Barca", "Manchester United", "Bayern de Munique|Bayern", "Liverpool", "Juventus", "Milan", "PSG|Paris Saint-Germain", "Chelsea", "Manchester City"}
};

void envia(char *msg) {
    char buf[200];
    sprintf(buf, "%s\n", msg);
    send(sock, buf, strlen(buf), 0);
}

int recebe(char *buf) {
    int i = 0;
    char c;
    while (recv(sock, &c, 1, 0) == 1) {
        if (c == '\n') {
            buf[i] = '\0';
            return 1;
        }
        if (i < 198) buf[i++] = c;
    }
    return 0;
}

void limpa(char *orig, char *dest) {
    int i, k = 0;
    for (i = 0; orig[i] != '\0'; i++) {
        if (isalnum((unsigned char)orig[i])) dest[k++] = tolower((unsigned char)orig[i]);
    }
    dest[k] = '\0';
}

void nome_item(int i, char *dest) {
    strcpy(dest, itens[j.lista][i]);
    char *p = strchr(dest, '|');
    if (p) *p = '\0';
}

int procura(char *palpite) {
    char a[200], b[60], copia[60];
    int i;
    limpa(palpite, a);
    if (strlen(a) == 0) return -1;
    for (i = 0; i < 10; i++) {
        strcpy(copia, itens[j.lista][i]);
        char *parte = strtok(copia, "|");
        while (parte) {
            limpa(parte, b);
            if (strcmp(a, b) == 0) return i;
            parte = strtok(NULL, "|");
        }
    }
    return -1;
}

void mostra() {
    int i;
    char nome[60];
    printf("\n==================================================\n");
    printf(" %s\n", titulos[j.lista]);
    printf("==================================================\n");
    for (i = 0; i < 10; i++) {
        if (j.achado[i]) {
            nome_item(i, nome);
            printf(" %2d. %-25s (%s)\n", i + 1, nome, j.nome[j.achado[i]]);
        } else {
            printf(" %2d. ??????\n", i + 1);
        }
    }
    printf("--------------------------------------------------\n");
    printf(" %s: %d pts   |   %s: %d pts\n", j.nome[1], j.pontos[1], j.nome[2], j.pontos[2]);
}

void trata(char *msg) {
    int quem = msg[0] - '0';
    char tipo = msg[1];
    char *resto = msg + 2;
    char nome[60];
    int i, total = 0;

    if (tipo == 'N') {
        strcpy(j.nome[quem], resto);
    } else if (tipo == 'L') {
        j.lista = atoi(resto);
    } else if (tipo == 'A') {
        i = atoi(resto) - 1;
        j.achado[i] = quem;
        j.pontos[quem] += i + 1;
        j.passou = 0;
        nome_item(i, nome);
        printf("\n>> %s ACERTOU o numero %d: %s (+%d pontos)\n", j.nome[quem], i + 1, nome, i + 1);
        for (i = 0; i < 10; i++) if (j.achado[i]) total++;
        if (total == 10) j.fim = 1;
        j.vez = 3 - quem;
    } else if (tipo == 'E') {
        j.passou = 0;
        printf("\n>> %s chutou \"%s\" e ERROU\n", j.nome[quem], resto);
        j.vez = 3 - quem;
    } else if (tipo == 'P') {
        j.passou++;
        printf("\n>> %s passou a vez\n", j.nome[quem]);
        if (j.passou >= 2) j.fim = 1;
        j.vez = 3 - quem;
    } else if (tipo == 'S') {
        printf("\n>> %s saiu do jogo\n", j.nome[quem]);
        j.fim = 1;
    }
}

void *thread_recebe(void *arg) {
    char msg[200];
    while (recebe(msg)) {
        pthread_mutex_lock(&trava);
        trata(msg);
        pthread_cond_signal(&sinal);
        pthread_mutex_unlock(&trava);
    }
    pthread_mutex_lock(&trava);
    j.fim = 1;
    pthread_cond_signal(&sinal);
    pthread_mutex_unlock(&trava);
    return NULL;
}

void conecta() {
    WSADATA wsa;
    struct sockaddr_in end;
    char ip[50];
    int op;

    WSAStartup(MAKEWORD(2, 2), &wsa);
    printf("1 - Criar sala\n2 - Entrar na sala\nOpcao: ");
    scanf("%d", &op);
    getchar();

    end.sin_family = AF_INET;
    end.sin_port = htons(PORTA);

    if (op == 1) {
        SOCKET servidor = socket(AF_INET, SOCK_STREAM, 0);
        end.sin_addr.s_addr = INADDR_ANY;
        bind(servidor, (struct sockaddr *)&end, sizeof(end));
        listen(servidor, 1);
        printf("Esperando o outro jogador entrar...\n");
        sock = accept(servidor, NULL, NULL);
        closesocket(servidor);
        eu = 1;
    } else {
        printf("IP da sala (Enter = 127.0.0.1): ");
        fgets(ip, 50, stdin);
        ip[strcspn(ip, "\n")] = '\0';
        if (strlen(ip) == 0) strcpy(ip, "127.0.0.1");
        sock = socket(AF_INET, SOCK_STREAM, 0);
        end.sin_addr.s_addr = inet_addr(ip);
        if (connect(sock, (struct sockaddr *)&end, sizeof(end)) != 0) {
            printf("Nao foi possivel conectar.\n");
            exit(1);
        }
        eu = 2;
    }
    outro = 3 - eu;
    printf("Conectado! Voce e o jogador %d\n", eu);
}

int main() {
    char msg[200], palpite[150], nome[30], item[60];
    int i;

    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));
    memset(&j, 0, sizeof(j));

    printf("========== TOP 10 ==========\n");
    printf("Seu nome: ");
    fgets(nome, 30, stdin);
    nome[strcspn(nome, "\n")] = '\0';
    if (strlen(nome) == 0) strcpy(nome, "Jogador");

    conecta();

    sprintf(msg, "%dN%s", eu, nome);
    trata(msg);
    envia(msg);
    recebe(msg);
    trata(msg);

    if (eu == 1) {
        printf("\nListas:\n");
        for (i = 0; i < 10; i++) printf(" %d - %s\n", i + 1, titulos[i]);
        printf("Escolha a lista (0 = sortear): ");
        scanf("%d", &i);
        getchar();
        if (i < 1 || i > 10) i = rand() % 10 + 1;
        sprintf(msg, "1L%d", i - 1);
        trata(msg);
        envia(msg);
    } else {
        printf("Esperando %s escolher a lista...\n", j.nome[1]);
        recebe(msg);
        trata(msg);
    }

    j.vez = 1;
    pthread_t t;
    pthread_create(&t, NULL, thread_recebe, NULL);

    while (1) {
        pthread_mutex_lock(&trava);
        if (j.vez != eu && !j.fim) printf("\nVez de %s, aguarde...\n", j.nome[outro]);
        while (j.vez != eu && !j.fim) pthread_cond_wait(&sinal, &trava);
        if (j.fim) {
            pthread_mutex_unlock(&trava);
            break;
        }
        mostra();
        pthread_mutex_unlock(&trava);

        printf("\nSUA VEZ! Digite um palpite sem acento (0 = passar, sair = sair)\n");
        do {
            printf("Palpite: ");
            if (fgets(palpite, 150, stdin) == NULL) strcpy(palpite, "sair");
            palpite[strcspn(palpite, "\n")] = '\0';
            for (i = 0; palpite[i]; i++) if (palpite[i] == '|') palpite[i] = ' ';

            if (strcmp(palpite, "0") == 0) {
                sprintf(msg, "%dP", eu);
            } else if (strcmp(palpite, "sair") == 0) {
                sprintf(msg, "%dS", eu);
            } else if (strlen(palpite) == 0) {
                msg[0] = '\0';
            } else {
                i = procura(palpite);
                if (i >= 0 && j.achado[i]) {
                    nome_item(i, item);
                    printf("%s ja foi achado, tenta outro.\n", item);
                    msg[0] = '\0';
                } else if (i >= 0) {
                    sprintf(msg, "%dA%d", eu, i + 1);
                } else {
                    sprintf(msg, "%dE%s", eu, palpite);
                }
            }
        } while (msg[0] == '\0');

        pthread_mutex_lock(&trava);
        trata(msg);
        pthread_mutex_unlock(&trava);
        envia(msg);
    }

    mostra();
    printf("\n========== FIM DE JOGO ==========\n");
    printf("A lista completa era:\n");
    for (i = 0; i < 10; i++) {
        nome_item(i, item);
        printf(" %2d. %s\n", i + 1, item);
    }
    if (j.pontos[1] > j.pontos[2]) printf("\n%s VENCEU!\n", j.nome[1]);
    else if (j.pontos[2] > j.pontos[1]) printf("\n%s VENCEU!\n", j.nome[2]);
    else printf("\nEMPATE!\n");

    closesocket(sock);
    WSACleanup();
    printf("\nAperte Enter para sair...");
    getchar();
    return 0;
}
