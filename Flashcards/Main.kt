package flashcards

import java.io.File
import java.lang.Integer.max
import kotlin.random.Random

fun main(args: Array<String>) {
  val flashCard = FlashCard()
  // Handle CLI parameters
  var exportFileName: String? = null
  for (i in args.indices) {
    when (args[i]) {
      "-import" -> flashCard.import(args[i + 1])
      "-export" -> exportFileName = args[i + 1]
    }
  }

  // Flashcards program starts here
  var action: String
  do {
    flashCard.log("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    action = readln()
    flashCard.log(action, true)

    when (action) {
      "add" -> flashCard.add()
      "remove" -> flashCard.remove()
      "import" -> flashCard.import(null)
      "export" -> flashCard.export(null)
      "ask" -> flashCard.ask()
      "log" -> flashCard.log(null)
      "hardest card" -> flashCard.hardestCard()
      "reset stats" -> flashCard.resetStats()
      else -> flashCard.log("Bye bye!")
    }
  } while (action != "exit")

  exportFileName?.let { flashCard.export(it) }
}

// Make a class to wrap all function and data together
class FlashCard {
  data class FlashCardItem(val card: String, val description: String, var wrongCount: Int = 0)

  private val flashCards: MutableList<FlashCardItem> = mutableListOf()
  private val logHistory: MutableList<String> = mutableListOf()

  /**
   * Define a custom splitter for importing and exporting.
   * I have not used ":" since it is a very common character
   * and there are high chances of it being in the description itself.
   */
  private val splitter = " 1:1:1 "
  val randomInt: (Int) -> Int = { Random(50).nextInt(it) }

  fun ask() {
    log("How many times to ask?")

    val times = readln().toInt()
    log(times.toString(), true)

    if (flashCards.isEmpty()) {
      log("No cards present")
      return
    }

    for (i in 0 until times) {
      val flashCard = flashCards[randomInt(flashCards.size)]
      log("Print the definition of \"${flashCard.card}\"")

      val answer = readln()
      log(answer, true)

      if (answer == flashCard.description) {
        log("Correct!")
      } else {
        flashCard.wrongCount += 1
        val correctAnswer = flashCards.find { it.description == answer }
        if (correctAnswer != null) {
          log(
            "Wrong. The right answer is \"${flashCard.description}\", but your definition is correct for \"${correctAnswer.card}\""
          )
        } else {
          log("Wrong. The right answer is \"${flashCard.description}\"")
        }
      }
    }
  }

  fun add() {
    log("The Card:")

    val card = readln()
    log(card, true)

    if (flashCards.find { it.card == card } != null) {
      log("The card \"$card\" already exists.\n")
      return
    }

    log("The definition of the card:")

    val definition = readln()
    log(definition, true)

    if (flashCards.find { it.description == definition } != null) {
      log("The definition \"$definition\" already exists.\n")
      return
    }
    flashCards.add(FlashCardItem(card, definition))
    log("The pair (\"$card\":\"$definition\") has been added.\n")
  }

  fun remove() {
    log("Which card?")

    val card = readln()
    log(card, true)

    if (flashCards.removeIf { it.card == card }) {
      log("The card has been removed.")
    } else {
      log("Can't remove \"$card\": there is no such card.")
    }
  }

  private fun getFile(): File {
    log("File name:")

    val fileName = readln()
    log(fileName, true)

    return File(fileName)
  }

  fun import(fileName: String?) {
    val file = fileName?.let { File(it) } ?: getFile()

    if (!file.exists()) {
      log("File not found.\n")
      return
    }
    var i = 0

    file.forEachLine {
      val (card, description, wrongCount) = it.split(splitter)
      flashCards.add(FlashCardItem(card, description, wrongCount.toInt()))
      i++
    }
    log("$i cards have been loaded.")
  }

  fun export(fileName: String?) {
    val file = fileName?.let { File(fileName) } ?: getFile()
    file.writeText("")
    for ((card, description, wrongCount) in flashCards) {
      file.appendText("$card$splitter$description$splitter$wrongCount\n")
    }
    log("${flashCards.size} cards have been saved.")
  }

  fun log(str: String?, isInput: Boolean = false) {
    if (str != null) {
      logHistory.add(str)
      if (!isInput) {
        println(str)
      }
    } else {
      val file = getFile()
      file.writeText("")
      logHistory.forEach {
        file.appendText("$it\n")
      }
      log("The log has been saved.")
    }
  }

  fun hardestCard() {
    var maxError = 0
    flashCards.forEach { maxError = max(it.wrongCount, maxError) }
    if (maxError == 0) {
      log("There are no cards with errors.")
      return
    }
    val hardestCards: List<FlashCardItem> = flashCards.filter { it.wrongCount == maxError }
    if (hardestCards.size > 1) {
      log(
        "The hardest cards are ${
          hardestCards.map { "\"${it.card}\", " }.joinToString { it }
        }. You have ${maxError * hardestCards.size} errors answering them."
      )
    } else {
      log("The hardest card is \"${hardestCards[0].card}\". You have ${hardestCards[0].wrongCount} errors answering it")
    }
  }

  fun resetStats() {
    flashCards.forEach { it.wrongCount = 0 }
    log("Card statistics have been reset.")
  }
}